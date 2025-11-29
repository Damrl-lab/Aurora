#!/usr/bin/env python3
import os, sys
import pandas as pd


# import of db_config.py from the parent directory
script_dir = os.path.dirname(__file__)              
parent_dir = os.path.dirname(script_dir)            
sys.path.append(parent_dir)
from db_config import get_connection

# ────────────────────────────────────────────────────────────────────
# Excel path
EXCEL_PATH = "data_sources/Cleaned_Dataset/sample_students_and_enrollments.xlsx"
# ────────────────────────────────────────────────────────────────────

# 1) Load “Students” sheet
df = pd.read_excel(EXCEL_PATH, sheet_name="Students")

# 2) Prepare rows for upsert
#    Users_Students columns: user_id, first_name, last_name,
#                            email, status, career_interest, password_hash
rows = [
    (
        row["user_id"],
        row["first_name"],
        row["last_name"],
        row["email"],
        row["status"],
        row["career_interest"],
        row["password_hash"]
    )
    for _, row in df.iterrows()
]

# 3) Upsert into Users_Students
SQL = """
INSERT INTO Users_Students
    (user_id, first_name, last_name, email,
     status, career_interest, password_hash)
VALUES (%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (user_id) DO UPDATE
  SET first_name       = EXCLUDED.first_name,
      last_name        = EXCLUDED.last_name,
      email            = EXCLUDED.email,
      status           = EXCLUDED.status,
      career_interest  = EXCLUDED.career_interest,
      password_hash    = EXCLUDED.password_hash;
"""

def load_user_student():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(SQL, rows)
        print(f"✅  Upserted {len(rows)} students into Users_Students.")
    finally:
        conn.close()
