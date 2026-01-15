# ── router_api / main.py ────────────────────────────────────────────
from __future__ import annotations
import os, re, textwrap, httpx, calendar, time
from datetime import date
import asyncio
import datetime
import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ── CONFIG ───────────────────────────────────────────────────────────
user = os.getenv("POSTGRES_USER")
pw   = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST", "vector_db")
port = os.getenv("POSTGRES_PORT", "5432")
db   = os.getenv("POSTGRES_DB")
PG_DSN = os.getenv("PG_DSN") or f"postgresql://{user}:{pw}@{host}:{port}/{db}"

for i in range(10):
    try:
        conn = psycopg.connect(PG_DSN, autocommit=True)
        break
    except psycopg.OperationalError:
        print(f"[router_api] waiting for DB ({i+1}/10)…"); time.sleep(3)
else:
    raise RuntimeError("Postgres not reachable")

VALIDATOR_URL = os.getenv("VALIDATOR_URL", "http://prolog_kb:8000")


# ─────────────────── Data models ──────────────────────────────────

class Filter(BaseModel):
    skill_ids      : list[int]  = Field(default_factory=list)
    semester       : str | None = None
    credit_cap     : int | None = None
    student_courses: list[str]  = Field(default_factory=list)
    program        : str | None = None
    user_id        : int | None = None
    long_term      : bool = False
    year           : int | None = None
    q              : str
    course_limit   : int | None = None 

class CandidateResponse(BaseModel):
    prompt     : str
    course_ids : list[str]
    warning    : str | None = None 

class RoadmapResponse(BaseModel):
    prompt : str
    plan   : list[dict]   # [{semester:"Fall 25", courses:[...]}]
    warning: str | None = None
    
class CheckPrereqRequest(BaseModel):
    user_id: int
    course_id: str

class CheckPrereqResponse(BaseModel):
    intent:     str
    course:     str
    eligible:   bool
    all_prereqs: list[str]
    completed:  list[str]
    prompt:     str

class ExplainReqRequest(BaseModel):
    course_id: str
    user_id:   int | None = None

class ExplainReqResponse(BaseModel):
    intent:                   str
    target_course:            str
    prerequisite:             str | None
    target_description:       str | None
    target_prerequisites:     list[str]
    prerequisite_description: str | None
    explanation:              str

class CreditInfoRequest(BaseModel):
    course_id: str

class CreditInfoResponse(BaseModel):
    intent:       str
    course:       str
    title:        str
    credits:      int
    description:  str
    prompt:       str

app = FastAPI(title="Course-Advisor · Router")

# ─────────────────── Helpers ───────────────────────────────────────
_month_re = re.compile(r"\b(" + "|".join(calendar.month_name[1:]) + r")\b", re.I)
COURSE_RE = re.compile(r"\b([A-Z]{2,4})[_\-\s]?(\d{3,4})\b")

def check_term_offering_warning(semester: str | None) -> str | None:
    """
    Check if the database has term-offering metadata.
    Returns a warning message if the data is missing, None otherwise.
    """
    if not semester:
        return None
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 1
              FROM information_schema.columns
             WHERE table_name='courses'
               AND column_name='terms_offered'
        """)
        has_terms = cur.fetchone() is not None
    if not has_terms:
        return (
            f"⚠️ I don't have data on which courses are offered in "
            f"{semester}. These recommendations ignore term availability."
        )
    return None

def _normalize_id(cid: str) -> str:
    """
    Convert your DB course_id (e.g. "COP_2210") into the Prolog atom form ("cop2210").
    """
    return re.sub(r"[^A-Za-z0-9]", "", cid).lower()

def _skill_names(ids: list[int]) -> list[str]:
    """Convert skill IDs to skill names for display in prompts."""
    if not ids:
        return []
    with conn.cursor() as cur:
        cur.execute("SELECT skill_name FROM skills WHERE skill_id=ANY(%s)", (ids,))
        return [r[0] for r in cur.fetchall()]

def get_student_context(user_id: int) -> tuple[str | None, list[str]]:
    """
    Fetch student's active program and course history.
    Returns (program_id, list_of_taken_course_ids).
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT mo.program_id,
                   COALESCE(m.major_name, mo.program_name)
              FROM user_program up
              JOIN program_offerings mo USING(program_id)
         LEFT JOIN majors m USING(major_id)
             WHERE up.user_id=%s
               AND up.status = 'active'
          ORDER BY up.start_date DESC
             LIMIT 1
        """, (user_id,))
        row = cur.fetchone()

        cur.execute("SELECT course_id FROM user_course WHERE user_id=%s", (user_id,))
        taken = [r[0] for r in cur.fetchall()]
    return (row[0], taken) if row else (None, taken)

def extract_course_id(raw: str) -> str:
    """Normalize “cap-4630” → “CAP_4630”. """
    m = COURSE_RE.search(raw.upper())
    if not m:
        raise ValueError(f"Invalid course format: {raw}")
    return f"{m.group(1)}_{m.group(2)}"

def completed_courses(user_id: int) -> list[str]:
    """
    Fetch user's completed courses from user_course.
    Note: Similar function exists in intent_ner (returns set instead of list).
    Kept separate as services run in isolated containers.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT course_id
              FROM user_course
             WHERE user_id = %s
               AND status = 'completed'
        """, (user_id,))
        return [r[0].upper() for r in cur.fetchall()]
    
def infer_next_term_year(semester: str) -> int:
    """Infer the calendar year for the next occurrence of a given semester."""
    today = datetime.date.today()
    yr, mo = today.year, today.month
    sem = semester.lower()
    if sem == "fall":
        return yr if mo < 9 else yr + 1
    if sem == "spring":
        return yr + 1 if mo >= 9 else yr
    if sem == "summer":
        return yr if mo < 6 else yr
    return yr

async def _prolog_stub(cid: str) -> dict[str, str]:
    """
    Ask prolog_kb for title/credits if the course is missing in Postgres.
    Falls back to sensible defaults.
    """
    title = "(title unavailable)"
    try:
        async with httpx.AsyncClient(timeout=5.0) as cli:
            r = await cli.post(f"{VALIDATOR_URL}/course_title",
                               json={"course": cid})
            r.raise_for_status()
            data  = r.json()
            title = data.get("title", "(title unavailable)")
            found = True        # JSON came back OK
    except Exception:
        found = False
    return {
        "course_id": cid,
        "course_title": title if found else "(unknown course)",
        "course_description": "",
        "credits": "n/a",
    }

async def make_course_blocks(cur: psycopg.Cursor,
                            ids: list[str]) -> tuple[str, list[str]]:
    """
    Build COURSE_FACT blocks for the given course IDs.
    Returns (formatted_blocks_string, list_of_confirmed_ids).
    Falls back to Prolog KB if course not found in Postgres.
    """
    if not ids:
        return "", []
    cur.execute("""
        SELECT course_id, course_title, LEFT(course_description,350), credits
          FROM courses
         WHERE course_id = ANY(%s)
    """, (ids,))
    in_db = {row[0]: row for row in cur.fetchall()}          # id -> row
    blocks, confirmed = [], []

    for cid in ids:                                          # keep caller’s order
        if cid in in_db:
            cid_, title, desc, cr = in_db[cid]
        else:
            stub = await _prolog_stub(cid)
            cid_, title, desc, cr = (stub["course_id"],
                                     stub["course_title"],
                                     stub["course_description"],
                                     stub["credits"])
        confirmed.append(cid_)
        blocks.append(f"""### COURSE_FACT
id: {cid_}
title: {title.strip()}
description: {(desc or '').strip()}
credits: {cr}
""")
    return "\n".join(blocks), confirmed

def build_prompt(raw_q: str, f: Filter, ctx_blocks: str, top_ids: list[str]) -> str:
    """
    Build a structured 5W+1H prompt for the LLM.
    Combines student query, context blocks, and chain-of-thought frame.
    """
    who = f.program or "unknown major"
    if f.user_id and not f.program:
        major, _ = get_student_context(f.user_id)
        who = major or who

    what = raw_q[:80] + ("…" if len(raw_q) > 80 else "")
    if f.semester:
        year = f.year or infer_next_term_year(f.semester)
        when = f"{f.semester} {year}"
    else:
        when = _month_re.search(raw_q).group(1) if _month_re.search(raw_q) else "any time"
    why  = ", ".join(_skill_names(f.skill_ids)) or "…"
    if top_ids:
        lines = []
        for cid in top_ids:
            # find the raw chain (if any)
            pat = rf"### PREREQ_CHAIN for {cid}\n([^\n]+)"
            m = re.search(pat, ctx_blocks)
            if m:
                raw = [s.strip() for s in m.group(1).split(",")]
                # skip if it's just [cid]
                if raw != [cid.lower()]:
                    chain = " → ".join(raw)
                    lines.append(f"- {cid} (prereqs: {chain})")
                    continue
            lines.append(f"- {cid}")
        top = "\n".join(lines)
    else:
        top = "(none)"

    cot = textwrap.dedent(f"""\
        ### CHAIN-OF-THOUGHT FRAME
        - WHO: {who}
        - WHAT: {what}
        - WHEN: {when}
        - WHERE: n/a
        - WHY:  {why}
        - HOW:  through the courses listed above
    """)

    return textwrap.dedent(f"""\
        **Student Query**
        {raw_q}

        **Context Blocks**
        {ctx_blocks}

        **Candidate Courses:**
        {top}

        {cot}
    """)


# ─────────────────── 1. Immediate recommendations ──────────────────
@app.post("/candidate_ids", response_model=CandidateResponse)
async def candidate_ids(f: Filter):
    if f.user_id is None:
        raise HTTPException(400, "candidate_ids requires user_id")

    # 1) Load student context
    major, taken = get_student_context(f.user_id)
    if not major:
        raise HTTPException(404, "No active program found for this user")
    prog_atom = major.lower().replace('-', '_')
    f.program = prog_atom
    f.student_courses = taken
    if f.semester and f.year is None:
        f.year = infer_next_term_year(f.semester)

    # check for missing term‐offering metadata
    warning = check_term_offering_warning(f.semester)

    # 2) Load ALL program courses + core flag + year
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                course_id,
                is_core,
                recommended_year
            FROM program_course
            WHERE program_id = %s
        """, (major,))
        rows = cur.fetchall()
    all_ids   = [r[0] for r in rows]
    core_set  = {r[0] for r in rows if r[1]}
    # replace NULL years with a high sentinel so sorting never sees None
    year_map  = {r[0]: (r[2] if r[2] is not None else 999) for r in rows}

    # 3) Apply skill/credit filters if present
    if f.skill_ids or f.credit_cap is not None:
        sql = """
          SELECT DISTINCT pc.course_id
            FROM program_course pc
       LEFT JOIN course_skill cs USING(course_id)
       LEFT JOIN courses c USING(course_id)
           WHERE pc.program_id = %(program)s
             AND (%(has_skills)s AND cs.skill_id = ANY(%(skills)s) OR NOT %(has_skills)s)
             AND (%(has_cap)s AND c.credits <= %(cap)s OR NOT %(has_cap)s)
             AND pc.course_id <> ALL(%(taken)s)
        """
        params = {
            "program":    major,
            "skills":     f.skill_ids,
            "has_skills": bool(f.skill_ids),
            "cap":        f.credit_cap or 0,
            "has_cap":    f.credit_cap is not None,
            "taken":      taken,
        }
        with conn.cursor() as cur:
            cur.execute(sql, params)
            candidate_ids = [r[0] for r in cur.fetchall()]
    else:
        candidate_ids = all_ids

    # 4) Drop already completed
    candidate_ids = [c for c in candidate_ids if c not in taken]

    # 5) Split into core vs elective
    cores     = [c for c in candidate_ids if c in core_set]
    electives = [c for c in candidate_ids if c not in core_set]

    # 6) Helper to ask Prolog which of a given list is immediately takeable
    async def prolog_ready(subset: list[str]) -> list[str]:
        if not subset:
            return []
        atoms = [ _normalize_id(c) for c in subset ]
        payload = {
            "student_courses": taken,
            "credit_cap":      f.credit_cap,
            "semester":        (f.semester or "any").lower(),
            "program":         prog_atom,
            "candidate_ids":   atoms,
        }
        try:
            r = await httpx.AsyncClient().post(
                f"{VALIDATOR_URL}/recommend_now", json=payload, timeout=20.0
            )
            r.raise_for_status()
            rec = r.json().get("recommended", [])
            # map back to DB IDs
            return [ c for c in subset if _normalize_id(c) in rec ]
        except:
            # fallback: return whole subset
            return subset

    ready_cores     = await prolog_ready(cores)
    ready_electives = await prolog_ready(electives)

    # 7) Merge cores+electives (or only electives if requested)
    if re.search(r"\belectives?\b", f.q, re.I):
        ready = ready_electives
    else:
        ready = ready_cores + ready_electives

    # 7.a) Guard to enforce any “one-of” groups so we never return both members (e.g. you can take MAD_2104 OR COT_3100)
    ONE_OF_GROUPS = [
        ["MAD_2104", "COT_3100"],
    ]
    for group in ONE_OF_GROUPS:
        chosen = [c for c in ready if c in group]
        if len(chosen) > 1:
            for loser in chosen[1:]:
                ready.remove(loser)

    # 8) Sort within each bucket by recommended_year
    ready.sort(key=lambda c: year_map.get(c, 999))

    # 9) Apply any explicit course_limit
    if f.course_limit is not None:
        ready = ready[: f.course_limit]

    # 10) Enforce credit cap
    if f.credit_cap is not None:
        trimmed, total = [], 0
        with conn.cursor() as cur:
            for cid in ready:
                cur.execute(
                    "SELECT COALESCE(credits,0) FROM courses WHERE course_id=%s",
                    (cid,),
                )
                cr = cur.fetchone()[0]
                if total + cr <= f.credit_cap:
                    trimmed.append(cid)
                    total += cr
        ready = trimmed

    # 11) Build context & prompt 
    chains = {}
    async with httpx.AsyncClient(timeout=20.0) as cli:
        for cid in all_ids:
            try:
                r = await cli.post(
                    f"{VALIDATOR_URL}/needed_chain",
                    json={
                        "target":          cid,
                        "student_courses": taken,
                        "program":         prog_atom,
                    },
                )
                r.raise_for_status()
                chains[cid] = r.json().get("chain", [])
            except:
                chains[cid] = []
    with conn.cursor() as cur:
        taken_block = "### STUDENT_HISTORY\n" + ", ".join(sorted(taken)) + "\n"
        course_block, confirmed = await make_course_blocks(cur, ready)

        chain_block = ""
        for cid in confirmed:
            if chains.get(cid):
                chain_block += f"### PREREQ_CHAIN for {cid}\n"
                chain_block += ", ".join(chains[cid]) + "\n"

        ctx = taken_block + course_block + chain_block

    prompt = build_prompt(f.q, f, ctx, confirmed)
    return {"prompt": prompt, "course_ids": confirmed, "warning": warning}




# ─────────────────── 2. Long-term roadmap ──────────────────────────
def build_roadmap_prompt(raw_q: str, f: Filter, plan: list[dict]) -> str:
    """Build a structured prompt for multi-semester degree planning."""
    who = f.program or "unknown major"
    # label WHEN line as e.g. “Fall 2025”
    when = f"{f.semester} {f.year}" if f.semester else "next available term"
    history = "### STUDENT_HISTORY\n" + ", ".join(sorted(f.student_courses)) + "\n\n"
    # each block in plan already reads “Fall 2025”, “Spring 2026”, etc.
    bullets = "\n".join(
        f"- **{block['semester']}**: {', '.join(block['courses'])}"
        for block in plan
    )

    return textwrap.dedent(f"""\
        **Student Query**
        {raw_q}
        
        **Completed Courses**
        {history}

        **Computed Degree Plan**
        {bullets}

        ### FRAME
        - WHO: {who}
        - WHAT: produce multi-semester roadmap
        - WHEN: {when}
        - WHY: complete degree efficiently
        - HOW: prerequisite DAG scheduling
    """)

@app.post("/roadmap", response_model=RoadmapResponse)
async def roadmap(f: Filter):
    if f.user_id is None:
        raise HTTPException(400, "roadmap endpoint requires user_id")

    # ── 1. student context ───────────────────────────────────────
    major_id, taken = get_student_context(f.user_id)
    if not major_id:
        raise HTTPException(404, "No active programme for this user")

    prog_atom = major_id.lower().replace('-', '_')  # "cs_bs"
    start_sem = (f.semester or "Fall").lower()
    f.program = prog_atom
    f.student_courses = taken
    
    if f.semester and f.year:
        today = date.today()
        # last month for each term
        end_month = {"Spring":5, "Summer":8, "Fall":12}[f.semester.capitalize()]
        # if already past, roll forward one term
        if (f.year < today.year) or (f.year == today.year and today.month > end_month):
            # advance term
            next_map = {"Spring":"Summer", "Summer":"Fall", "Fall":"Spring"}
            f.semester = next_map[f.semester.capitalize()]
            # bump year if we wrapped from Fall → Spring
            if f.semester == "Spring":
                f.year += 1
    else:
        # you already have your infer_next_term_year logic here
        f.year = infer_next_term_year(start_sem)
    # if  changed f.semester in the roll-forward block, we can recompute start_sem here:
    start_sem = (f.semester or "Fall").lower()
    
    if f.year is None:
        f.year = infer_next_term_year(start_sem)

    payload = {
        "program":        prog_atom,
        "taken":          taken,
        "credit_cap":     f.credit_cap or 15,
        "start_semester": start_sem,
    }
    
    warning = check_term_offering_warning(f.semester)

    # ── 2. call Prolog planner ───────────────────────────────────
    try:
        r = await httpx.AsyncClient().post(f"{VALIDATOR_URL}/roadmap",
                       json=payload, timeout=30.0)
        print("[router] ← status", r.status_code, flush=True)
        r.raise_for_status()
        plan = r.json()["plan"]
        year_counter = f.year
        for block in plan:
            sem = block["semester"]          # e.g. "Fall"
            block["semester"] = f"{sem} {year_counter}"
            if sem.lower() == "fall":
                year_counter += 1
    except httpx.HTTPError as e:
        print("[router] EXCEPTION", repr(e), flush=True)
        raise HTTPException(502, f"prolog_kb error: {e}")

    prompt = build_roadmap_prompt(f.q, f, plan)
    if warning:
        prompt = warning + "\n\n" + prompt
        
    resp = {"prompt": prompt, "plan": plan}
    if warning:
        resp["warning"] = warning
    return resp



# ─────────────────── 3a) Check Prerequisite ─────────────────────────
@app.post("/check_prerequisite", response_model=CheckPrereqResponse)
async def check_prerequisite(req: CheckPrereqRequest):
    target = req.course_id.upper()
    atom   = _normalize_id(target)

    # 1) ask Prolog for prereq list
    prereqs: list[str] = []
    try:
        r = await httpx.post(f"{VALIDATOR_URL}/prereqs",
                             json={"course": atom}, timeout=10.0)
        r.raise_for_status()
        pl = r.json()
        if pl.get("found"):
            prereqs = [p.upper() for p in pl["prerequisites"]]
    except Exception:
        pass

    # 2) fetch user’s completed courses
    taken = completed_courses(req.user_id)

    # 3) decide eligibility
    eligible = all(p in taken for p in prereqs)

    # 4) build a mini‐prompt for your LLM
    completed_block = "\n".join(f"- {c}" for c in sorted(taken)) or "(none)"
    prereq_block    = "\n".join(f"- {p}" for p in prereqs)         or "(none)"
    prompt = f"""**Student Query**
Check prerequisites for {target}

**Context Blocks**
### COMPLETED_COURSES
{completed_block}

**Required prerequisites**
{prereq_block}

"""

    return {
        "intent":       "check-prerequisite",
        "course":       target,
        "eligible":     eligible,
        "all_prereqs":  prereqs,
        "completed":    taken,
        "prompt":       prompt,
    }


# ─────────────────── 3b) Explain Requirement ─────────────────────────
@app.post("/explain_requirement", response_model=ExplainReqResponse)
async def explain_requirement(req: ExplainReqRequest):
    target = req.course_id.upper()
    atom   = _normalize_id(target)

    # 1) get all prereqs from Prolog
    target_prereqs: list[str] = []
    try:
        r = await httpx.post(f"{VALIDATOR_URL}/prereqs",
                             json={"course": atom}, timeout=10.0)
        r.raise_for_status()
        pl = r.json()
        if pl.get("found"):
            target_prereqs = [p.upper() for p in pl["prerequisites"]]
    except Exception:
        pass

    # 2) pull descriptions from your courses table
    prereq = target_prereqs[0] if target_prereqs else None
    with conn.cursor() as cur:
        cur.execute("SELECT course_description FROM courses WHERE course_id=%s",
                    (target,))
        row = cur.fetchone()
        target_desc = row[0] if row else None

        prereq_desc = None
        if prereq:
            cur.execute("SELECT course_description FROM courses WHERE course_id=%s",
                        (prereq,))
            row = cur.fetchone()
            prereq_desc = row[0] if row else None

    # 3) craft an explanation
    if prereq:
        explanation = (f"{target} builds directly on material taught in "
                       f"{prereq}, so it is required first.")
    elif target_prereqs:
        explanation = (f"{target} lists {', '.join(target_prereqs)} "
                       f"as prerequisites.")
    else:
        explanation = (f"I don’t see any prerequisites listed for {target}. "
                       "If you need more detail, check the catalog or ask an advisor.")

    return {
        "intent":                   "explain-requirement",
        "target_course":            target,
        "prerequisite":             prereq,
        "target_description":       target_desc,
        "target_prerequisites":     target_prereqs,
        "prerequisite_description": prereq_desc,
        "explanation":              explanation,
    }


# ─────────────────── 3c) Credit Lookup ───────────────────────────────
@app.post("/credit_info", response_model=CreditInfoResponse)
async def credit_info(req: CreditInfoRequest):
    cid = req.course_id.upper()

    with conn.cursor() as cur:
        cur.execute("""
           SELECT course_title, credits, course_description
             FROM courses
            WHERE course_id = %s
        """, (cid,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(404, f"Course {cid} not found.")
        title, credits, desc = row

    prompt = f"""**Student Query**
How many credits is {cid}?

**COURSE_FACT**
id: {cid}
title: {title}
description: {(desc or '').strip()}
credits: {credits}

"""

    return {
        "intent":      "credit-info",
        "course":      cid,
        "title":       title,
        "credits":     credits,
        "description": desc,
        "prompt":      prompt,
    }

