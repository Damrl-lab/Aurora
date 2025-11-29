"""
load_academic_advisor_student.py
--------------------------------
Links each student to a matching academic advisor and upserts the rows
into Academic_Advisor_Student (advisor_email, user_id, start_date).

Logic
-----
* Advisors are pulled from Academic_Advisor and grouped by their
  `graduate_undergrad` flag ('UG' vs 'G').
* Active programme enrolments in User_Program determine whether a student
  is undergraduate or graduate:
      • Programme IDs that start with  'MS', 'PHD', 'MA', …  → graduate
      • everything else                                    → undergraduate
* Students are distributed round-robin across the advisor pool for their
  level, so the loader remains deterministic yet balanced.
* `start_date` is the earliest programme start date found for that
  student (fallback: today).
* `ON CONFLICT (advisor_email, user_id)` keeps the loader idempotent.
"""

import os, sys
from pathlib import Path
from datetime import date

# ── import get_connection ---------------------------------------
script_dir = Path(__file__).resolve().parent
sys.path.append(str(script_dir.parent))          
from db_config import get_connection             


# ────────────────────────────────────────────────────────────────
# 1. Fetch helpers
# ────────────────────────────────────────────────────────────────
def fetch_advisors(cur):
    """Return {'UG': [email,…], 'G': [email,…]}."""
    cur.execute("""
        SELECT advisor_email, graduate_undergrad
        FROM   Academic_Advisor
    """)
    levels = {"UG": [], "G": []}
    for email, lvl in cur.fetchall():
        if not email:
            continue
        key = "G" if (lvl and lvl.upper().startswith("G")) else "UG"
        levels[key].append(email)
    return levels


def fetch_student_programs(cur):
    """
    Return {user_id: [(program_id, start_date, end_date), …]}.
    We grab *all* enrolments; active-only filtering isn’t critical here.
    """
    cur.execute("""
        SELECT user_id, program_id, start_date, end_date
        FROM   User_Program
    """)
    mapping = {}
    for uid, prog, sd, ed in cur.fetchall():
        mapping.setdefault(uid, []).append((prog, sd, ed))
    return mapping


# ────────────────────────────────────────────────────────────────
# 2. Heuristic to label a programme as UG / G
# ────────────────────────────────────────────────────────────────
_GRAD_PREFIXES = ("MS", "PHD", "MA", "MBA", "MENG", "MTEC")


def infer_level(program_id: str) -> str:
    return "G" if program_id and program_id.upper().startswith(_GRAD_PREFIXES) else "UG"


# ────────────────────────────────────────────────────────────────
# 3. Build (advisor_email, user_id, start_date) rows
# ────────────────────────────────────────────────────────────────
def build_rows(advisors, student_programs):
    ug_pool, g_pool = advisors["UG"], advisors["G"]
    ug_i = g_i = 0
    rows = []

    for uid, enrolments in student_programs.items():
        # classify the student (any graduate programme makes them grad)
        levels = {infer_level(p) for p, *_ in enrolments}
        level = "G" if "G" in levels else "UG"

        pool = g_pool if level == "G" else ug_pool
        if not pool:          # no advisor of that level in the DB yet
            continue

        advisor_email = pool[g_i % len(pool)] if level == "G" \
                       else pool[ug_i % len(pool)]

        if level == "G":
            g_i += 1
        else:
            ug_i += 1

        # earliest start_date found, fallback = today
        sdate = min((sd for _, sd, _ in enrolments if sd), default=date.today())
        rows.append((advisor_email, uid, sdate))

    return rows


# ────────────────────────────────────────────────────────────────
# 4. Upsert
# ────────────────────────────────────────────────────────────────
SQL = """
INSERT INTO Academic_Advisor_Student
      (advisor_email, user_id, start_date)
VALUES (%s, %s, %s)
ON CONFLICT (advisor_email, user_id) DO UPDATE
      SET start_date = EXCLUDED.start_date;
"""


def load_academic_advisor_student():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            advisors         = fetch_advisors(cur)
            student_programs = fetch_student_programs(cur)
            rows             = build_rows(advisors, student_programs)

            if rows:
                cur.executemany(SQL, rows)
                print(f"✅  Upserted {len(rows)} advisor–student links.")
            else:
                print("ℹ️  No rows to upsert.")
    finally:
        conn.close()


