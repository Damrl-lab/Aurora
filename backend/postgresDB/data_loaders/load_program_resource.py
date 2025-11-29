import os, sys

# import db_config.py from parent dir
script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)
from db_config import get_connection

# ──────────────────────────────────────────────────────────────────
# 1) Program → opportunity names mapping (as before)
# ──────────────────────────────────────────────────────────────────
common_undergrad = [
    "Peer Tutoring (STARS & ASI)",
    "UKG Academy for Computer Science and Education - Programming Team",
    "ACM Student Chapter",
    "Women in CS (WiCS)",
    "Women in CyberSecurity (WiCyS)",
    "KFSCIS Seminar Series",
    "Workshops & Short Courses",
    "Hackathons",
    "Tech Talent Academy",
    "Break Through Tech Miami (BTT FIU)",
    "FIU Discovery Lab"
]

ms_only = [
    "Graduate Applications Office",
    "Career & Talent Development"
]

phd_only = [
    "Data Management Research Laboratory (DaMRL)",
    "Bioinformatics Research Group (BioRG)",
    "SOLID Lab",
    "CAESCIR",
    "Southeast Florida Coastal Environmental Data & Modeling Center",
    "Center for Diversity in Engineering & Computing"
]

PROGRAM_RESOURCE = {
    # Undergraduates
    "CS-BA":     common_undergrad,
    "CS-BS":     common_undergrad,
    "CS-BS-SDD": common_undergrad,
    "CS-MINOR":  common_undergrad,
    "DS-BS":     common_undergrad,
    "IT-BA":     common_undergrad,
    "IT-BS":     common_undergrad,
    "IT-BS-SW":  common_undergrad,

    # Master’s
    "MS-CS":     common_undergrad + ms_only,
    "MS-DS":     common_undergrad + ms_only,

    # PhD
    "PHD-CS":    common_undergrad + ms_only + phd_only,
}

# ──────────────────────────────────────────────────────────────────
# 2) Fetch opportunity_name → opportunity_id
# ──────────────────────────────────────────────────────────────────
def fetch_opportunity_set(cur):
    cur.execute("SELECT opportunity_name FROM Additional_Opportunities;")
    return {row[0] for row in cur.fetchall()}

# ──────────────────────────────────────────────────────────────────
# 3) Build rows: (program_id, opportunity_id, notes)
# ──────────────────────────────────────────────────────────────────
def build_rows(valid_ops):
    rows, skipped = [], {}
    for prog_id, names in PROGRAM_RESOURCE.items():
        for name in names:
            if name not in valid_ops:
                skipped.setdefault(prog_id, []).append(name)
                continue
            note = ("Graduate only" if prog_id.startswith("MS-") or prog_id == "PHD-CS"
                    else "Undergraduate only")
            rows.append((prog_id, name, note))

    for prog, missing in skipped.items():
        print(f"⚠️  {prog}: missing opportunities → {', '.join(missing)}")
    return rows

# ──────────────────────────────────────────────────────────────────
# 4) Upsert into Program_Resource (now: program_id, opportunity_id, notes)
# ──────────────────────────────────────────────────────────────────
SQL = """
INSERT INTO Program_Resource
      (program_id, opportunity_name, notes)
VALUES (%s, %s, %s)
ON CONFLICT (program_id, opportunity_name) DO UPDATE
      SET notes = EXCLUDED.notes;
"""

def load_program_resource():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            valid_ops = fetch_opportunity_set(cur)
            rows      = build_rows(valid_ops)
            if rows:
                cur.executemany(SQL, rows)
                print(f"✅  Upserted {len(rows)} program–opportunity links.")
            else:
                print("ℹ️  Nothing to upsert.")
    finally:
        conn.close()
