import os
import sys
from datetime import datetime

# import of db_config.py from the parent directory
script_dir = os.path.dirname(__file__)              
parent_dir = os.path.dirname(script_dir)            
sys.path.append(parent_dir)
from db_config import get_connection


MAJORS = [
    # major_id,        major_name,            department
    ("CS", "Computer Science",                "Knight Foundation School of Computing & Information Sciences"),
    ("DS", "Data Science",                    "Knight Foundation School of Computing & Information Sciences"),
    ("IT", "Information Technology",          "Knight Foundation School of Computing & Information Sciences"),
    ("PM", "Product Management Certificate",  "FIU College of Business – Executive Education"),
]

def load_majors():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO Majors (major_id, major_name, department)
                VALUES (%s, %s, %s)
                ON CONFLICT (major_id) DO UPDATE
                    SET major_name = EXCLUDED.major_name,
                        department  = EXCLUDED.department;
                """,
                MAJORS,
            )
        print(f"✅  Loaded {len(MAJORS)} majors @ {datetime.now():%Y-%m-%d %H:%M}")
    finally:
        conn.close()