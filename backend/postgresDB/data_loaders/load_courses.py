import os
import re
import pandas as pd
from datetime import datetime, timezone
from pdfminer.high_level import extract_text
import sys

# import of db_config.py from the parent directory
script_dir = os.path.dirname(os.path.abspath(__file__))  # data_loaders/
parent_dir = os.path.dirname(script_dir)                 # postgres_schema/
sys.path.append(parent_dir)

from db_config import get_connection 

# -------------------------------------------------------------------
# Folder path containing all course PDFs (easier to extract info about courses from)
# -------------------------------------------------------------------
EXCEL_PATH = "data_sources/Cleaned_Dataset/cleaned_all_courses.xlsx"
PDF_DIR    = "data_sources/all_courses"
DEPT       = "Knight Foundation School of Computing & Information Sciences"

# --------------- regex patterns ---------------------------------
TITLE_RE      = re.compile(r"course title:\s*(.*?)\s*date", re.I | re.S)
DESC_RE       = re.compile(r"catalog_description:\s*(.*?)\s*textbook", re.I | re.S)
CREDITS_RE    = re.compile(r"credits?:\s*(\d+)", re.I)
PREREQ_RE     = re.compile(r"prereq(?:uisite)?\w*:\s*(.+?)(?:course outcomes:|$)", re.I | re.S)
OUTCOMES_RE   = re.compile(r"course outcomes:\s*(.+)", re.I | re.S)

PDF_TITLE_RE  = re.compile(r"^[A-Z]{3}[_ ]?\d{4}\s*[-–]?\s*(.+)", re.M)
PDF_DESC_RE   = re.compile(r"Course Description:\s*(.+?)(?:Prereq|Pre-requisite|$)", re.I | re.S)
PDF_PREREQ_RE = re.compile(r"Pre[- ]requisite[s]?:\s*(.+)", re.I)
PDF_OUTCOME_RE= re.compile(r"course learning outcomes.*?:\s*(.+)", re.I | re.S)

def first(regex, text, cast=lambda x: x):
    m = regex.search(text)
    return cast(m.group(1).strip()) if m else None

def derive_level(code: str) -> str | None:
    m = re.search(r"\d{3,4}", code)
    return "UG" if m and int(m.group()) < 5000 else "G"

def syllabus_url(code: str) -> str:
    return f"https://www4.cis.fiu.edu/courses/Syllabi/{code}.pdf"

# ------------ PDF fallback ---------------------------------------
def parse_pdf(code: str) -> dict:
    pdf_path = os.path.join(PDF_DIR, f"{code}.pdf")
    if not os.path.exists(pdf_path):
        return {}
    try:
        text = extract_text(pdf_path)
    except Exception as e:
        print(f"⚠️  PDF parse failed for {code}: {e}")
        return {}
    return {
        "course_title":       first(PDF_TITLE_RE,  text),
        "course_description": first(PDF_DESC_RE,   text),
        "prerequisites":      first(PDF_PREREQ_RE, text),
        "outcomes":           first(PDF_OUTCOME_RE,text),
    }

# ------------ load spreadsheet -----------------------------------
df = pd.read_excel(EXCEL_PATH)
if not {"Course Name", "Course Description"}.issubset(df.columns):
    raise ValueError("Excel missing required columns.")

rows = []
for _, rec in df.iterrows():
    cid  = str(rec["Course Name"]).strip()
    blob = str(rec["Course Description"])

    # initial parse from Excel blob
    title  = first(TITLE_RE,   blob)
    descr  = first(DESC_RE,    blob)
    credits= first(CREDITS_RE, blob, int)
    prereq = first(PREREQ_RE,  blob)
    outc   = first(OUTCOMES_RE, blob)

    if not title or not descr:
        pdf_data = parse_pdf(cid) or {}
        title  = title  or pdf_data.get("course_title")     or cid
        descr  = descr  or pdf_data.get("course_description")
        prereq = prereq or pdf_data.get("prerequisites")
        outc   = outc   or pdf_data.get("outcomes")

    rows.append((
        cid,
        title or cid,              # ensure NOT NULL
        blob,                      # syllabus_text ← entire raw blob ✅
        prereq,
        credits,
        DEPT,
        derive_level(cid),
        None,                      # semester_offered (still NULL for now)
        descr,
        None,                      # faculty_email
        syllabus_url(cid),
        None,                      # capacity
        outc,
        datetime.now(timezone.utc)
    ))

# ------------- upsert ---------------------------------------------
SQL = """
INSERT INTO Courses
  (course_id, course_title, syllabus_text, prerequisites, credits,
   department, level, semester_offered, course_description,
   faculty_email, course_url, capacity, outcomes, last_updated)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (course_id) DO UPDATE SET
   course_title       = EXCLUDED.course_title,
   syllabus_text      = EXCLUDED.syllabus_text,
   prerequisites      = EXCLUDED.prerequisites,
   credits            = EXCLUDED.credits,
   department         = EXCLUDED.department,
   level              = EXCLUDED.level,
   course_description = EXCLUDED.course_description,
   course_url         = EXCLUDED.course_url,
   outcomes           = EXCLUDED.outcomes,
   last_updated       = EXCLUDED.last_updated;
"""

def load_courses():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(SQL, rows)
        print(f"✅  Loaded/updated {len(rows)} courses (with PDF fallback).")
    finally:
        conn.close()