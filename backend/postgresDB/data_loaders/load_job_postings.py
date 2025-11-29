"""
load_job_postings.py  –  Insert / upsert postings from the 5 Excel files
------------------------------------------------------------------------
Expected table columns (per schema):
    employer, job_title, location, job_description, job_url,
    posting_date, expiration_date, job_type,
    min_salary, max_salary, application_deadline, category_id

• Assumes a UNIQUE index on job_url for idempotent upsert, e.g.:
      CREATE UNIQUE INDEX IF NOT EXISTS uq_joburl ON Job_Postings(job_url);

• Excel files are expected in CLEAN_DIR with names:
      cs_jobs.xlsx, ds_jobs.xlsx, it_jobs.xlsx, swe_jobs.xlsx, pm_jobs.xlsx
"""

import os, sys, re, pandas as pd
from datetime import datetime, timezone
from dateutil import parser as dtparse

# import of db_config.py from the parent directory
script_dir = os.path.dirname(__file__)              
parent_dir = os.path.dirname(script_dir)            
sys.path.append(parent_dir)
from db_config import get_connection

CLEAN_DIR = "data_sources/Cleaned_Dataset"
FILES = {
    "cs_jobs.xlsx":  "CS",
    "ds_jobs.xlsx":  "DS",
    "it_jobs.xlsx":  "IT",
    "swe_jobs.xlsx": "SWE",
    "pm_jobs.xlsx":  "PM",
}

def parse_date(val):
    if pd.isna(val) or str(val).strip() == "":
        return None
    if isinstance(val, (pd.Timestamp, datetime)):
        return val.to_pydatetime().astimezone(timezone.utc)
    try:
        return dtparse.parse(str(val)).astimezone(timezone.utc)
    except Exception:
        return None

_money_re = re.compile(r"([\d,\.]+)")
def parse_money(val):
    if pd.isna(val):
        return None
    m = _money_re.search(str(val))
    return float(m.group(1).replace(",", "")) if m else None

rows = []
for fname, cat in FILES.items():
    path = os.path.join(CLEAN_DIR, fname)
    if not os.path.exists(path):
        print(f"⚠️  {fname} not found – skipped")
        continue

    df = pd.read_excel(path)
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

    for _, r in df.iterrows():
        rows.append((
            r.get("employer")  or r.get("company"),
            r.get("job_title") or r.get("title"),
            r.get("location"),
            r.get("description"),                  
            r.get("job_url")   or r.get("url"),
            parse_date(r.get("posting_date") or r.get("date_posted")),
            parse_date(r.get("expiration_date")),
            r.get("job_type")  or r.get("type"),
            parse_money(r.get("min_amount") or r.get("salary_min")),
            parse_money(r.get("max_amount") or r.get("salary_max")),
            r.get("currency"),                     
            cat
        ))

print(f"Prepared {len(rows)} posting rows.")

SQL = """
INSERT INTO Job_Postings
  (employer, job_title, location, job_description, job_url,
   posting_date, expiration_date, job_type,
   min_salary, max_salary, currency, category_id)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (job_url) DO UPDATE SET
   employer            = EXCLUDED.employer,
   job_title           = EXCLUDED.job_title,
   location            = EXCLUDED.location,
   job_description     = EXCLUDED.job_description,
   posting_date        = EXCLUDED.posting_date,
   expiration_date     = EXCLUDED.expiration_date,
   job_type            = EXCLUDED.job_type,
   min_salary          = EXCLUDED.min_salary,
   max_salary          = EXCLUDED.max_salary,
   currency            = EXCLUDED.currency,
   category_id         = EXCLUDED.category_id;
"""

def load_jobs():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(SQL, rows)
        print(f"✅  Loaded / updated {len(rows)} job postings.")
    finally:
        conn.close()