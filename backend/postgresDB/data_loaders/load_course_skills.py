# load_course_skill.py  –  strict mapper (Skills → Course_Skill)
import re, os, sys

# import of db_config.py from the parent directory
script_dir = os.path.dirname(__file__)              
parent_dir = os.path.dirname(script_dir)            
sys.path.append(parent_dir)
from db_config import get_connection

def build_regex(name: str) -> re.Pattern:
    return re.compile(rf"\b{re.escape(name.lower())}\b")

SQL = """
INSERT INTO Course_Skill (course_id, skill_id, coverage_level)
VALUES (%s,%s,%s)
ON CONFLICT (course_id, skill_id) DO NOTHING;
"""

def load_course_skill():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # 1) load vetted skills
            cur.execute("SELECT skill_id, skill_name FROM Skills")
            skill_rows = [(sid, sname.lower(), build_regex(sname)) for sid, sname in cur.fetchall()]

            # 2) load course text
            cur.execute("""
                SELECT course_id,
                       COALESCE(outcomes,'') || ' ' || COALESCE(course_description,'')
                FROM Courses
            """)
            courses = cur.fetchall()

            rows = []
            for cid, blob in courses:
                text = blob.lower()
                for sid, sname, pat in skill_rows:
                    if pat.search(text):
                        rows.append((cid, sid, "core"))

            cur.executemany(SQL, rows)
        conn.commit()
        print(f"✅  Linked {len(rows)} Course→Skill rows.")
    finally:
        conn.close()
