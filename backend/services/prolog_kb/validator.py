"""
Prolog Knowledge Base Validator Service

Provides a REST API facade over SWI-Prolog for prerequisite checking,
eligibility validation, and multi-semester roadmap planning.
"""
from __future__ import annotations

import os, re, subprocess
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
import textwrap

# ── CONFIG ───────────────────────────────────────────────────────────
app       = FastAPI(title="Prolog-KB Validator")
PROLOG_KB = os.path.join(os.getcwd(), "rules_loader.pl")
DEBUG     = bool(os.getenv("DEBUG_PROLOG"))

_COURSE_RX = re.compile(r"[A-Za-z0-9]+")   # course atoms (used by atoms_from_list_literal)
_PROG_RX   = re.compile(r"[A-Za-z0-9_]+")  # programme atoms may keep underscores


# ──────────────────────── helpers ─────────────────────────────
def norm_course(s: str) -> str:
    """'MAC-2312' → 'mac2312'   •   'cgs_1920' → 'cgs1920'"""
    s = re.sub(r"[^A-Za-z0-9]", "", s.lower())
    return ("c_" + s) if not s or not s[0].isalpha() else s


def norm_prog(s: str) -> str:
    """'CS-BS-SSD' → 'cs_bs_ssd'"""
    return _PROG_RX.findall(s.lower().replace(" ", "_").replace("-", "_"))[0] if s else ""


def atoms_from_list_literal(txt: str) -> list[str]:
    """Convert `format('~q',[List])` output to a Python list."""
    return [m.lower() for m in _COURSE_RX.findall(txt)]


# ───────────────────── SWI-Prolog bridge ──────────────────────
def run_prolog(goal: str) -> str:
    """Run *goal* once; raise 500 on any non-zero exit code."""
    proc = subprocess.run(
        ["swipl", "-q", "-s", PROLOG_KB, "-g", goal, "-t", "halt"],
        capture_output=True, text=True,
    )
    if proc.returncode:
        _dump_failure(goal, proc)
        raise HTTPException(500, proc.stderr or "Prolog error")
    return proc.stdout.strip()


def _dump_failure(goal: str, p: subprocess.CompletedProcess[str]) -> None:
    print("\n=== SWI-Prolog FAILED ===")
    print("GOAL  :", goal)
    print("STDOUT:", p.stdout or "∅")
    print("STDERR:", p.stderr or "∅", flush=True)


def _maybe_dump(goal: str, raw: str) -> None:
    if DEBUG:
        print("\n--- PROLOG GOAL ---\n", goal)
        print("--- PROLOG RAW  ---\n", raw, flush=True)


# ──────────────────────── models ──────────────────────────────
class EligibilityRequest(BaseModel):
    student_courses: List[str]
    target: str


class PrereqRequest(BaseModel):
    course: str


class ValidationFilters(BaseModel):
    student_courses: List[str] = Field(default_factory=list)
    credit_cap: Optional[int]  = None
    semester:   Optional[str]  = None      # “Fall”, “Spring”, …
    program:         Optional[str] = None   # "cs_bs" or "ms_cs"


class ValidateIDsRequest(BaseModel):
    candidate_ids: List[str]
    filters:       ValidationFilters


class RoadmapRequest(BaseModel):
    program        : str                 # "cs_bs"
    taken          : list[str]
    credit_cap     : int = 15
    start_semester : str = "fall"


class RoadmapResponse(BaseModel):
    plan: list[dict]

class RecommendNowRequest(BaseModel):
    candidate_ids: Optional[List[str]] = None
    student_courses: List[str]  = Field(default_factory=list)
    credit_cap: Optional[int]   = None
    semester:   Optional[str]   = None
    program:    Optional[str]   = None

class RecommendNowResponse(BaseModel):
    recommended: List[str]

class ChainRequest(BaseModel):
    target: str
    student_courses: List[str]
    program: str | None = None 
    
class RequiredCoursesRequest(BaseModel):
    program: str

class RequiredCoursesResponse(BaseModel):
    required: List[str]

# ───────────────────────── routes ─────────────────────────────
@app.post("/eligible")
def eligible(req: EligibilityRequest):
    taken  = "[" + ",".join(norm_course(c) for c in req.student_courses) + "]"
    target = norm_course(req.target)
    goal   = f"(can_take({target},{taken}) -> write(yes) ; write(no))"
    return {"eligible": run_prolog(goal) == "yes"}


@app.post("/prereqs")
def prereqs(req: PrereqRequest):
    atom = norm_course(req.course)
    if run_prolog(f"(course({atom}) -> write(yes) ; write(no))") != "yes":
        return {"course": req.course, "found": False,
                "prerequisites": [], "message": "not in KB"}

    goal = (f"findall(S,(prerequisite({atom},P),atom_string(P,S)),L),"
            f"format('~q',[L])")
    lst  = atoms_from_list_literal(run_prolog(goal))
    return {"course": req.course, "found": True, "prerequisites": lst}

@app.post("/needed_chain")
def needed_chain(req: ChainRequest):
    prog   = norm_prog(req.program) if req.program else ""
    tgt    = norm_course(req.target)
    taken  = "[" + ",".join(norm_course(c) for c in req.student_courses) + "]"

    # never let needed_chain/3 cause a Prolog failure:
    fmt_chain = "format('~q',[Chain])"
    fmt_empty = "format('~q',[[]])"
    if prog:
        folder = "graduate" if prog.startswith(("ms_", "phd_")) else "undergraduate"
        path   = f"flowchart_rules/{folder}/{prog}_rules.pl"
        goal   = (
            f"( consult('{path}'),"
            f"  ( needed_chain({tgt},{taken},Chain)"
            f"    -> {fmt_chain}"
            f"    ;  {fmt_empty}"
            f"  )"
            f")"
        )
    else:
        goal   = (
            f"(  ( needed_chain({tgt},{taken},Chain)"
            f"     -> {fmt_chain}"
            f"     ;  {fmt_empty}"
            f"    )"
            f")"
        )

    chain = atoms_from_list_literal(run_prolog(goal))
    return {"target": req.target, "chain": chain}


@app.post("/course_title")
def course_title(req: Dict[str, str] = Body(...)):
    atom  = norm_course(req["course"])
    title = run_prolog(f"title_or_stub({atom},Title),write(Title)")
    return {"course": req["course"], "title": title}

@app.post("/recommend_now", response_model=RecommendNowResponse)
def recommend_now(req: RecommendNowRequest):
    """Filter candidate courses to those immediately takeable based on prerequisites."""
    # — normalize & consult the proper flowchart for this program
    prog_atom = norm_prog(req.program) if req.program else ""
    consult_snip = f"load_program({prog_atom}), " if prog_atom else ""

    # — build Prolog list literals
    taken = "[" + ",".join(norm_course(c) for c in req.student_courses) + "]"
    cap   = str(req.credit_cap) if req.credit_cap is not None else "15"
    sem   = norm_course(req.semester) if req.semester else "any"

    if req.candidate_ids:
        cand_list = "[" + ",".join(norm_course(c) for c in req.candidate_ids) + "]"
        goal = textwrap.dedent(f"""
      ( {consult_snip}
        % 1) collect everything that is already eligible
        findall(ID,
          ( member(ID,{cand_list}),
            validate_id(ID,filters({taken},{cap},{sem}),keep,[])
          ),
          Ready
        ),
        % 2) if nothing is eligible, pick the first locked course
        %    and return its immediate prereqs (or use needed_chain/3)
        ( Ready = [] ->
            {cand_list} = [Next|_],
            % you can choose missing_courses/3 for direct prereqs,
            % or needed_chain/3 for the whole unlock path:
            needed_chain(Next,{taken},FirstCourses)
        ;   FirstCourses = Ready
        ),
        format('~q',[FirstCourses])
      )
    """)
    else:
        goal = textwrap.dedent(f"""
          ( {consult_snip}
            ( make_plan({prog_atom},{taken},{cap},{sem},P)
              -> P = [block(_Semester,FirstCourses)|_]
              ;  ( findall(C,(required(C),\\+member(C,{taken})),[Next|_]),
                   missing_courses(Next,{taken},FirstCourses)
                 )
            ),
            format('~q',[FirstCourses])
          )
        """)

    raw = run_prolog(goal)
    recommended = atoms_from_list_literal(raw)
    return {"recommended": recommended}


@app.post("/validate_ids")
def validate_ids(req: ValidateIDsRequest):
    # — load the student’s major into Prolog so validator_rules sees the right prerequisites
    if req.filters.program:
        prog   = norm_prog(req.filters.program)
        folder = "graduate" if prog.startswith(("ms_", "phd_")) else "undergraduate"
        path   = f"flowchart_rules/{folder}/{prog}_rules.pl"
        consult_snippet = f"consult('{path}'), "
    else:
        consult_snippet = ""

    stu   = "[" + ",".join(norm_course(c) for c in req.filters.student_courses) + "]"
    cap   = str(req.filters.credit_cap) if req.filters.credit_cap else "_"
    sem   = norm_course(req.filters.semester) if req.filters.semester else "any"
    filts = f"filters({stu},{cap},{sem})"

    cand  = "[" + ",".join(norm_course(cid) for cid in req.candidate_ids) + "]"
    goal = (
        f"( {consult_snippet}"
        f"  findall(ID,(member(ID,{cand}),"
        f"             validate_id(ID,{filts},keep,_)),Kept),"
        f"  format('~q',[Kept]) )"
    )
    kept  = set(atoms_from_list_literal(run_prolog(goal)))
    return {"kept_ids": [cid for cid in req.candidate_ids
                         if norm_course(cid) in kept]}

# ────────────────────  required_courses  ────────────────────────
@app.post("/required_courses", response_model=RequiredCoursesResponse)
def required_courses(req: RequiredCoursesRequest):
    prog_atom = norm_prog(req.program)
    run_prolog(f"load_program({prog_atom})")

    # collect all required/1
    goal = "findall(C, (user:required(C), atom_string(C,S)), L), format('~q',[L])"
    raw  = run_prolog(goal)

    ids = re.findall(r"[A-Za-z0-9]+", raw)
    courses = [s.upper() for s in ids]
    return {"required": courses}


# ──────────────────────── roadmap ─────────────────────────────
_BLOCK_RX = re.compile(r"block\(([^,]+),\[(.*?)\]\)")

def _parse_blocks(raw: str) -> list[dict]:
    out: list[dict] = []
    for m in _BLOCK_RX.finditer(raw):
        sem = m.group(1).title()
        crs = [c.strip().upper() for c in m.group(2).split(',') if c]
        out.append({"semester": sem, "courses": crs})
    return out


@app.post("/roadmap", response_model=RoadmapResponse)
def roadmap(req: RoadmapRequest):
    """Generate a multi-semester degree completion roadmap using Prolog's make_plan/5."""
    prog   = norm_prog(req.program)
    folder = "graduate" if prog.startswith(("ms_", "phd_")) else "undergraduate"
    path   = f"flowchart_rules/{folder}/{prog}_rules.pl"

    taken  = "[" + ",".join(norm_course(c) for c in req.taken) + "]"
    start  = req.start_semester.lower()
    cap    = req.credit_cap

    goal = (
        f"( consult('{path}'),"
        f"  (   make_plan({prog},{taken},{cap},{start},P)"
        f"  ->  true"
        f"  ;   prereq_plan({prog},{taken},{cap},{start},P)"
        f"  ),"
        f"  format('~q',[P]) )"
    )
    raw  = run_prolog(goal)
    _maybe_dump(goal, raw)

    plan = _parse_blocks(raw)
    if not plan:
        raise HTTPException(500, 'Planner produced empty plan')
    return {'plan': plan}
