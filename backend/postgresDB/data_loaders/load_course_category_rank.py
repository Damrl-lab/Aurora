"""
load_course_category_rank.py
────────────────────────────
Populate Course_Category_Rank from the “compare_models” directory.

Folder layout:
    compare_models/
        CS/course_rankings.xlsx
        DS/course_rankings.xlsx
        IT/course_rankings.xlsx
        SWE/course_rankings.xlsx
        PM/course_rankings.xlsx
Each workbook has columns:  Course Name | Average_Course_Rank
"""

import os, sys, pandas as pd
from datetime import datetime, timezone

# import of db_config.py from the parent directory
script_dir = os.path.dirname(__file__)              
parent_dir = os.path.dirname(script_dir)            
sys.path.append(parent_dir)
from db_config import get_connection

BASE_DIR = "data_sources/compare_models"
CATEGORIES = ["CS", "DS", "IT", "SWE", "PM"]

UPSERT_SQL = """
INSERT INTO Course_Category_Rank
  (category_id, course_id, rank_pos, alignment_dt)
VALUES (%s,%s,%s,%s)
ON CONFLICT (category_id, course_id) DO UPDATE
  SET rank_pos    = EXCLUDED.rank_pos,
      alignment_dt= EXCLUDED.alignment_dt;
"""

def load_rankings() -> list[tuple]:
    rows = []
    utc_now = datetime.now(timezone.utc)
    for cat in CATEGORIES:
        fpath = os.path.join(BASE_DIR, cat, "course_rankings.xlsx")
        if not os.path.exists(fpath):
            print(f"⚠️  File missing for {cat}: {fpath} – skipped")
            continue

        df = pd.read_excel(fpath)
        # normalise column names
        df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

        if "course_name" not in df.columns or "average_course_rank" not in df.columns:
            print(f"⚠️  Unexpected columns in {fpath} – skipped")
            continue

        for _, r in df.iterrows():
            cid  = str(r["course_name"]).strip()
            rank = int(r["average_course_rank"])
            rows.append((cat, cid, rank, utc_now))
    return rows

def load_course_rank():
    rows = load_rankings()
    print(f"Prepared {len(rows)} (category, course) rows.")
    if not rows:
        return

    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(UPSERT_SQL, rows)
        print(f"✅  Loaded / updated {len(rows)} rows in Course_Category_Rank.")
    finally:
        conn.close()

