# ── intent_ner / main.py ────────────────────────────────────────────
import os
import re
from datetime import datetime
import httpx
import spacy
import psycopg2 as psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from spacy.matcher import PhraseMatcher

# ── CONFIG ───────────────────────────────────────────────────────────
user = os.getenv("POSTGRES_USER")
pw   = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST", "vector_db")
port = os.getenv("POSTGRES_PORT", "5432")
db   = os.getenv("POSTGRES_DB")

PG_DSN = os.getenv("PG_DSN") or f"postgresql://{user}:{pw}@{host}:{port}/{db}"

ROUTER_URL = os.getenv(
    "ROUTER_URL",
    "http://router_api:8000"
)

# ── NLP SETUP ─────────────────────────────────────────────────────────
nlp     = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# will fill in at startup
SKILL_MAP = {}

INTENT_RULES = {
    "recommend-courses": [
       r"\bwhat course\b",    r"\bwhich course\b",
       r"\brecommend\b",      r"\bsuggest\b",
       r"\bfocus on\b",       r"\bprepare for\b",
       r"\bplan\b",           r"\broadmap\b",
       r"\bdegree plan\b",    r"\blong[- ]term\b",
       r"\bschedule\b",       r"\bwhat should I take\b",
       r"\btake\b",
       r"\bfinish (?:my )?(?:degree|minor|program)\b",
       r"\bcomplete (?:my )?(?:degree|minor|program)\b",
    ],
    "check-prerequisite": [
       r"\bprereq(?:uisite)?\b",
       r"\beligible\b",
    ],
    "explain-requirement": [
       r"\bwhy\b",
       r"\breason for\b",
       r"\bneed to take\b",
    ],
    "credit-info": [
       r"\bhow many credits\b",
       r"\bcredit hours\b",
       r"\bcredits? (?:is|are)\b",
    ]
}

class Query(BaseModel):
    q: str
    user_id: int | None = None

app = FastAPI(title="Intent + NER + Router")


# ── LIFECYCLE: load skill names from Postgres into matcher ──────
@app.on_event("startup")
def startup():
    # 1) open connection
    conn = psycopg.connect(PG_DSN)
    conn.autocommit = True

    # 2) fetch all (skill_id, skill_name)
    with conn.cursor() as cur:
        cur.execute("SELECT skill_id, skill_name FROM Skills")
        rows = cur.fetchall()

    # 3) build lookup & PhraseMatcher patterns
    global SKILL_MAP
    SKILL_MAP = { name.lower(): sid for sid, name in rows }

    patterns = [ nlp.make_doc(name) for name in SKILL_MAP ]
    matcher.add("SKILL", patterns)

    conn.close()


# ── HELPERS ────────────────────────────────────────────────────────────

# helper to pull out course codes
COURSE_RE = re.compile(r"\b([A-Z]{2,4})[_\-\s]?(\d{3,4})\b")
def extract_courses(text: str) -> list[str]:
    """
    Returns a list of course IDs normalised to the DB style, e.g.
    “CAP 4630”, “CAP-4630”, “cap_4630” →  "CAP_4630"
    """
    ids = []
    for m in COURSE_RE.finditer(text.upper()):
        prefix, num = m.groups()
        ids.append(f"{prefix}_{num}")
    return ids

# helper to convert letters to numbers

WORD_NUMBERS = {
  "one":1, "two":2, "three":3, "four":4, "five":5,
  "six":6, "seven":7, "eight":8, "nine":9, "ten":10
}

def detect_intent(text: str) -> str:
    low = text.lower()
    
    # credit‐cap + “what/suggest/recommend” → recommend‐courses
    if re.search(r"\b\d+\s*credits?\b", text, re.I) \
       and re.search(r"\b(what|suggest|recommend)\b", low):
        return "recommend-courses"

    # 0) explicit credit lookup with course code → credit-info
    if re.search(r"\bhow many.*credits.*[A-Z]{2,4}[_\-\s]?\d{3,4}\b", text, re.I):
        return "credit-info"

    # 1) explicit “X before Y” → always check-prerequisite
    if PAT_BEFORE.search(text):
        return "check-prerequisite"

    # 2) credit-info, check-prerequisite or explain-requirement keywords
    for intent in ("credit-info", "check-prerequisite", "explain-requirement"):
        for kw in INTENT_RULES[intent]:
            if re.search(kw, text, re.I):
                # but “why” alone should only count if there’s a course code
                if intent == "explain-requirement" and kw.lower() == "why":
                    if extract_courses(text):
                        return "explain-requirement"
                    continue
                return intent

    # 3) true long-term roadmap keywords must come before generic “plan”
    if LONG_TERM_RE.search(text):
        return "recommend-courses"

    # 4) short-term next-semester plan → recommend-courses
    if SHORT_TERM_RE.search(text):
        return "recommend-courses"

    # 5) remaining recommend-courses keywords
    for pat in INTENT_RULES["recommend-courses"]:
        if re.search(pat, text, re.I):
            return "recommend-courses"

    return "generic"

def extract_filters(text: str):
    doc = nlp(text)
    
    def replace_word_num(m):
        return str(WORD_NUMBERS[m.group(0).lower()])
    text = re.sub(r"\b(" + "|".join(WORD_NUMBERS) + r")\b",
                  replace_word_num, text, flags=re.I)

    # phrase-match skills
    skills = [ SKILL_MAP[doc[start:end].text.lower()]
               for _, start, end in matcher(doc) ]

    # semester
    semester = None
    year     = None
    if re.search(r"\b(fall|autumn)\b", text, re.I):
        semester = "Fall"
    elif re.search(r"\bspring\b", text, re.I):
        semester = "Spring"
    elif re.search(r"\bsummer\b", text, re.I):
        semester = "Summer"
        
    # explicit year in text overrides defaults
    if y := re.search(r"\b(20\d{2})\b", text):
        year = int(y.group(1))
    
    # Figuring out the *upcoming* term:
    now = datetime.now()
    mo  = now.month
    if mo <= 4:
        upcoming = ("Spring", now.year)
    elif mo <= 7:
        upcoming = ("Summer", now.year)
    else:
        upcoming = ("Fall",   now.year)

    # if user named a semester but didn’t give a year, default to that upcoming year:
    if semester and year is None:
        if semester == upcoming[0]:
            year = upcoming[1]
        else:
            # find next occurrence of that semester after upcoming
            order = ["Spring","Summer","Fall"]
            idx_user = order.index(semester)
            idx_up   = order.index(upcoming[0])
            year = upcoming[1] + (1 if idx_user <= idx_up else 0)

    # handling “next SPRING” / “next FALL”:
    if semester and re.search(rf"\bnext\s+{semester.lower()}\b", text, re.I):
        # move one more cycle forward
        order = ["Spring","Summer","Fall"]
        idx = order.index(semester)
        next_idx = (idx + 1) % 3
        semester = order[next_idx]
        # bump year if wrapped around
        if next_idx == 0:  
            year = (year or now.year) + 1
        
    # credit cap
    credit_cap = None
    if m := re.search(r"\b(\d+)[-\s]*credit(?:s|\b)", text, re.I):
        credit_cap = int(m.group(1))
    
    # how many courses
    course_limit = None
    if m2 := re.search(
        r"\b(?:max(?:imum)?|suggest|show|pick)?\s*(\d+)\s+courses?\b",
        text, re.I
    ):
        course_limit = int(m2.group(1))  
        
    # long_term flag only if true-roadmap phrase appears
    long_term = bool(LONG_TERM_RE.search(text))
    
    if long_term:
        now = datetime.now()
        mo  = now.month
        if mo <= 4:
            semester, year = "Spring", now.year
        elif mo <= 7:
            semester, year = "Summer", now.year
        else:
            semester, year = "Fall",   now.year

    return skills, semester, credit_cap, long_term, year, course_limit
    

#  student history helper
def completed_courses(user_id: int) -> set[str]:
    """
    Return a set { "COP_2210", … } with all courses the student has completed.
    Note: Similar function exists in router_api (returns list instead of set).
    Kept separate as services run in isolated containers.
    """
    with psycopg.connect(PG_DSN) as c:
        cur = c.cursor()
        cur.execute("""
            SELECT course_id
              FROM user_course
             WHERE user_id = %s
               AND status   = 'completed'       
        """, (user_id,))
        return {row[0].upper() for row in cur.fetchall()}

# explicit-order patterns (need/before, take/before, …)
PAT_BEFORE = re.compile(
    r"\b(?:take|need|needs|requires?)\s+([A-Z]{2,4}[_\-\s]?\d{3,4})\s+before\s+([A-Z]{2,4}[_\-\s]?\d{3,4})",
    re.I
)

# long- vs short-term roadmap triggers (move these above detect_intent)
LONG_TERM_RE = re.compile(
    r"\b(?:plan the rest of|roadmap|degree plan|long[-\s]?term|plan of study"
    r"|final (?:academic )?year|graduate next"
    r"|finish\s+(?:my|the)?\s*(?:degree|minor|program)\b"
    r"|complete\b.+?\b(?:degree|minor|program)\b"
    r"|finish\b.*\bby\b"
    r")\b",
    re.I
)

SHORT_TERM_RE  = re.compile(r"\bplan (?:my )?(?:next semester|next term)\b", re.I)

# ── ENDPOINTS ─────────────────────────────────────────────────────────
@app.post("/parse")
async def parse(query: Query):
    intent      = detect_intent(query.q)
    skills, sem, cap, long_term, year, course_limit = extract_filters(query.q)

    return {
        "intent": intent,
        "filters": {
            "skill_ids":  skills,
            "semester":   sem,
            "year":      year,
            "credit_cap": cap,
            "long_term":  long_term,
            "course_limit": course_limit,
            "user_id":    query.user_id
        }
    }


@app.post("/recommend")
async def recommend(q: Query):
    parsed = await parse(q)
    intent = parsed["intent"]
    text   = q.q

    # ————————————————————————————————————
    # a) recommend‐courses
    # ————————————————————————————————————
    if intent == "recommend-courses":
        # must have a logged-in user
        if q.user_id is None:
            raise HTTPException(400, "You must be logged in to get course recommendations.")

        filters = parsed["filters"]
        filters.update({
            "q":        q.q,
            "user_id":  q.user_id,
        })
        
        endpoint = "roadmap" if filters.get("long_term") else "candidate_ids"
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{ROUTER_URL}/{endpoint}",
                    json=filters
                )
                resp.raise_for_status()
            except httpx.HTTPError as e:
                raise HTTPException(502, f"router_api error: {e}")

        return {
            "intent":     intent,
            "long_term": filters["long_term"],
            "filters":    filters,
            **resp.json(),
        }
    
    # ————————————————————————————————————
    # b) check‐prerequisite
    # ————————————————————————————————————
    if intent == "check-prerequisite":
        if q.user_id is None:
            raise HTTPException(400, "Must be logged in to check prerequisites.")
        # extract a single course code
        codes = extract_courses(text)
        if not codes:
            raise HTTPException(400, "Couldn’t find any course code in your question.")
        target_raw = codes[0].upper()
        payload = {"user_id": q.user_id, "course_id": target_raw}
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{ROUTER_URL}/check_prerequisite",
                                      json=payload)
        return resp.json()
    
    # ————————————————————————————————————
    # c) explain‐requirement → call router_api
    # ————————————————————————————————————
    if intent == "explain-requirement":
        codes = extract_courses(text)
        if not codes:
            raise HTTPException(400, "Couldn’t find any course code to explain.")
        payload = {"course_id": codes[0].upper(), "user_id": q.user_id}
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{ROUTER_URL}/explain_requirement",
                                      json=payload)
        return resp.json()

    # ————————————————————————————————————
    # d) credit-lookup → call router_api
    # ————————————————————————————————————
    if intent == "credit-info":
        codes = extract_courses(text)
        if not codes:
            raise HTTPException(400, "Couldn’t find a course code to look up credits.")
        payload = {"course_id": codes[0].upper()}
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{ROUTER_URL}/credit_info",
                                      json=payload)
        return resp.json()


    # ————————————————————————————————————
    # e) fallback for truly generic
    # ————————————————————————————————————
    return {
        "intent": intent,
        "text": (
            "I’m here to help you plan your courses. You can ask me to:\n"
            " • recommend courses for your major,\n"
            " • check if you’re eligible for a course,\n"
            " • explain why a course is required, or\n"
            " • look up how many credits a course is worth."
        ),
        "filters": parsed["filters"],
    }
