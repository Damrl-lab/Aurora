import os
import sys
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

# 1) Load the “User_Program” sheet
df = pd.read_excel(EXCEL_PATH, sheet_name="User_Program")

# 2) Prepare rows: the table has exactly these five columns now
rows = []
for _, row in df.iterrows():
    rows.append((
        row["user_id"],
        row["program_id"],
        row["start_date"],
        None if pd.isna(row["end_date"]) else row["end_date"],
        row["status"],
    ))

# 3) Upsert into User_Program, **without** catalog_year
SQL = """
INSERT INTO User_Program
    (user_id, program_id, start_date, end_date, status)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id, program_id) DO UPDATE
  SET start_date = EXCLUDED.start_date,
      end_date   = EXCLUDED.end_date,
      status     = EXCLUDED.status;
"""

def load_user_program():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(SQL, rows)
        print(f"✅  Upserted {len(rows)} enrollments into User_Program.")
    finally:
        conn.close()

