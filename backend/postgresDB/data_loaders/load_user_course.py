import os, sys, random
from datetime import datetime, timezone
import pandas as pd

# ── bootstrap so we can import get_connection ───────────────────────────────
script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)
from db_config import get_connection

# ────────────────────────────────────────────────────────────────────────────
EXCEL_PATH = "data_sources/Cleaned_Dataset/sample_students_and_enrollments.xlsx"
# ────────────────────────────────────────────────────────────────────────────

# grade pools
PASSING = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-"]
FAILING = ["D+", "D", "D-", "F"]

def pick_grade() -> str:
    return random.choice(PASSING) if random.random() < 0.9 else random.choice(FAILING)

def term_from_date_and_year(start_date, rec_year):
    """
    Given the student's start_date (a date) and
    this course's recommended_year (int),
    return something like "Fall 2023".
    """
    m = start_date.month
    if m >= 8:
        term = "Fall"
    elif m >= 5:
        term = "Summer"
    else:
        term = "Spring"
    year = start_date.year + (rec_year - 1)
    return f"{term} {year}"

def fetch_program_courses(cur):
    """
    Build mapping: program_id -> [ (course_id, recommended_year), ... ]
    """
    cur.execute("""
      SELECT program_id, course_id, recommended_year
        FROM Program_Course
    """)
    m = {}
    for prog, cid, rec in cur.fetchall():
        m.setdefault(prog, []).append((cid, rec))
    return m

def fetch_course_credits(cur):
    """
    Build mapping: course_id -> credits
    """
    cur.execute("SELECT course_id, credits FROM Courses")
    return { cid: credits or 0 for cid, credits in cur.fetchall() }

def is_undergrad(prog_code: str) -> bool:
    return prog_code.startswith(("CS-BA","CS-BS","CS-BS-SDD","CS-MINOR","DS-BS","IT-BA","IT-BS","IT-BS-SW"))

def credit_target(term: str, undergrad: bool):
    """
    term like "Fall 2023", "Summer 2022"
    """
    season = term.split()[0]
    if undergrad:
        if season == "Summer":
            return random.randint(6, 10)
        else:
            return random.randint(12, 18)
    else:
        if season == "Summer":
            return random.randint(5, 8)
        else:
            return random.randint(9, 12)

def load_user_course():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            prog_courses = fetch_program_courses(cur)
            course_credits = fetch_course_credits(cur)

        # load enrollments
        xls = pd.ExcelFile(EXCEL_PATH)
        df = pd.read_excel(xls, sheet_name="User_Program")

        today = datetime.now(timezone.utc).date()
        rows = []

        for _, r in df.iterrows():
            if pd.isna(r.start_date):
                continue

            uid   = int(r.user_id)
            prog  = r.program_id
            start = pd.to_datetime(r.start_date).date()
            years = (today - start).days // 365 + 1
            under = is_undergrad(prog)

            # group candidate courses by term
            terms_map = {}
            for cid, rec in prog_courses.get(prog, []):
                if rec is None or rec > years:
                    continue
                term = term_from_date_and_year(start, rec)
                terms_map.setdefault(term, []).append(cid)

            # for each term, pick courses up to target credits
            for term, cids in terms_map.items():
                target = credit_target(term, under)
                picked = []
                total = 0
                # shuffle and pick greedily
                random.shuffle(cids)
                for cid in cids:
                    cr = course_credits.get(cid, 3)
                    if total + cr <= target or not picked:
                        picked.append(cid)
                        total += cr
                    # stop once we hit/exceed target
                    if total >= target:
                        break

                # insert each picked course
                for cid in picked:
                    rows.append((
                        uid,
                        cid,
                        term,
                        pick_grade(),
                        "completed"
                    ))

        # upsert into User_Course
        SQL = """
        INSERT INTO User_Course
          (user_id, course_id, semester_taken, grade, status)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT (user_id, course_id) DO UPDATE
          SET semester_taken = EXCLUDED.semester_taken,
              grade          = EXCLUDED.grade,
              status         = EXCLUDED.status;
        """
        with conn, conn.cursor() as cur:
            cur.executemany(SQL, rows)

        print(f"✅  Upserted {len(rows)} User_Course records.")
    finally:
        conn.close()

