# load_job_skill.py  –  strict mapper (Skills → Job_Skill)
import re, os, sys

# import of db_config.py from the parent directory
script_dir = os.path.dirname(__file__)              
parent_dir = os.path.dirname(script_dir)            
sys.path.append(parent_dir)
from db_config import get_connection

def build_regex(name: str) -> re.Pattern:
    return re.compile(rf"\b{re.escape(name.lower())}\b")

SQL = """
INSERT INTO Job_Skill (job_id, skill_id, importance_level)
VALUES (%s,%s,%s)
ON CONFLICT (job_id, skill_id) DO NOTHING;
"""

def load_job_skill():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # 1) load vetted skills
            cur.execute("SELECT skill_id, skill_name FROM Skills")
            skill_rows = [(sid, sname.lower(), build_regex(sname)) for sid, sname in cur.fetchall()]

            # 2) load postings
            cur.execute("SELECT job_id, job_description FROM Job_Postings")
            postings = cur.fetchall()

            rows = []
            for job_id, desc in postings:
                if not desc:
                    continue
                text = desc.lower()
                for sid, sname, pat in skill_rows:
                    if pat.search(text):
                        rows.append((job_id, sid, "required"))

            cur.executemany(SQL, rows)
        conn.commit()
        print(f"✅  Linked {len(rows)} Job→Skill rows.")
    finally:
        conn.close()
