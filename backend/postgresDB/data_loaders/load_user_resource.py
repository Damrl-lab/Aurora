# load_user_resource.py
"""
Populate User_Resource (student ↔ opportunity memberships).

Assumptions
-----------
1. Users_Students and User_Program tables are already loaded.
2. Additional_Opportunities is populated and uses
   opportunity_name TEXT PRIMARY KEY.
3. The program→opportunity mapping (common_undergrad, ms_only, phd_only)
   matches the one used in load_program_resource.py.
"""

import os, sys
from pathlib import Path
from datetime import date

# ── import get_connection ─────────────────────────────────────────
script_dir = Path(__file__).resolve().parent
sys.path.append(str(script_dir.parent))
from db_config import get_connection

# ------------------------------------------------------------------
# 1) Program → opportunity mapping (reuse exactly the same lists)
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
# 2) Helpers to pull existing data from the DB
# ------------------------------------------------------------------
def fetch_opportunity_set(cur):
    cur.execute("SELECT opportunity_name FROM Additional_Opportunities;")
    return {row[0] for row in cur.fetchall()}

def fetch_user_programs(cur):
    """
    Returns dict: user_id → {program_id, program_id, …}
    Only active programs are considered (end_date IS NULL or in the future).
    """
    cur.execute("""
        SELECT user_id, program_id
        FROM   User_Program
        WHERE  end_date IS NULL OR end_date > CURRENT_DATE;
    """)
    user_prog = {}
    for uid, prog in cur.fetchall():
        user_prog.setdefault(uid, set()).add(prog)
    return user_prog

# ------------------------------------------------------------------
# 3) Build membership rows
# ------------------------------------------------------------------
def build_rows(user_prog, valid_ops):
    rows, skipped_ops = [], set()
    today = date.today()

    for uid, prog_set in user_prog.items():
        # Collect the union of opportunity lists for all of the student's programs
        opps = set()
        for prog in prog_set:
            opps.update(PROGRAM_RESOURCE.get(prog, []))

        for opp in opps:
            if opp not in valid_ops:
                skipped_ops.add(opp)
                continue
            rows.append((uid, opp, today, "Member"))

    if skipped_ops:
        print("⚠️  Opportunities not yet in DB (skipped):",
              ", ".join(sorted(skipped_ops)))
    return rows

# ------------------------------------------------------------------
# 4) Upsert into User_Resource
# ------------------------------------------------------------------
SQL = """
INSERT INTO User_Resource
      (user_id, opportunity_name, membership_date, role)
VALUES (%s, %s, %s, %s)
ON CONFLICT (user_id, opportunity_name) DO UPDATE
      SET membership_date = EXCLUDED.membership_date,
          role            = EXCLUDED.role;
"""

def load_user_resource():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            valid_ops   = fetch_opportunity_set(cur)
            user_prog   = fetch_user_programs(cur)
            rows        = build_rows(user_prog, valid_ops)

            if rows:
                cur.executemany(SQL, rows)
                print(f"✅  Upserted {len(rows)} student–opportunity memberships.")
            else:
                print("ℹ️  Nothing to upsert – no programs/opportunities matched.")
    finally:
        conn.close()

