import os, sys
from datetime import datetime

# add parent dir so we can import db_config
script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from db_config import get_connection

# ───────────────────────────────────────────────────────────────────────────
# 1) Existing advisors:
CTD_ADVISORS = [
    ("rutpache@fiu.edu", "Ruth E. Pacheco"),
    ("heclayto@fiu.edu", "Harold Clayton"),
    ("egduran@fiu.edu",  "Efigenia Gonzalez-Duran"),
    (None,              "Yisell Cirion"),
    ("dgregory@fiu.edu","Darren Gregory"),
    ("johnsona@fiu.edu","Audrey Johnson"),
    ("cebbage@fiu.edu", "Cristina Ebbage"),
    ("dmedina@fiu.edu", "Dante Medina"),
]

# 2) Existing opportunities (names only, for lookup below):
OPPORTUNITIES = [
    "Data Management Research Laboratory (DaMRL)",
    "Bioinformatics Research Group (BioRG)",
    "SOLID Lab",
    "CAESCIR",
    "Southeast Florida Coastal Environmental Data & Modeling Center",
    "Center for Diversity in Engineering & Computing",
    "Graduate Applications Office",
    "Peer Tutoring (STARS & ASI)",
    "UKG Academy for Computer Science and Education - Programming Team",
    "ACM Student Chapter",
    "Women in CS (WiCS)",
    "Women in CyberSecurity (WiCyS)",
    "Hackathons",
    "Workshops & Short Courses",
    "KFSCIS Seminar Series",
    "Tech Talent Academy",
    "Break Through Tech Miami (BTT FIU)",
    "FIU Discovery Lab",
    "Career & Talent Development",
]

# ───────────────────────────────────────────────────────────────────────────
# 3) “Best‐effort” recommendations: (advisor_email, opportunity_name, reason, priority, date_linked)
#    Match specialty → opportunity; everyone gets Career & Talent Dev; 
#    research‐lab advisors get their labs, etc.
ADVISOR_OPPORTUNITIES = [
    # ─ Ruth Pacheco (Industry Partnerships) ─
    ("rutpache@fiu.edu", "Career & Talent Development",
     "Central resource for all CTD offerings",          "High", datetime(2025,5, 1)),
    ("rutpache@fiu.edu", "Tech Talent Academy",
     "Bridges industry partnerships & micro-credentials", "Medium", datetime(2025,5, 1)),
    ("rutpache@fiu.edu", "Break Through Tech Miami (BTT FIU)",
     "Supports underrepresented groups in tech",          "Medium", datetime(2025,5, 1)),

    # ─ Harold Clayton (Campus Liaison) ─
    ("heclayto@fiu.edu","Peer Tutoring (STARS & ASI)",
     "Key peer-to-peer support for campus-wide students", "High", datetime(2025,5, 1)),
    ("heclayto@fiu.edu","ACM Student Chapter",
     "Ties into programming contests across campuses",   "Medium", datetime(2025,5, 1)),
    ("heclayto@fiu.edu","Hackathons",
     "Promotes collaborative campus events",             "Medium", datetime(2025,5, 1)),

    # ─ Efigenia Gonzalez‐Duran (Employer Engagement) ─
    ("egduran@fiu.edu", "Career & Talent Development",
     "Primary career services for employer-student matchmaking", "High", datetime(2025,5, 1)),
    ("egduran@fiu.edu", "Tech Talent Academy",
     "Prepares students for employer-led micro-credentials",    "High", datetime(2025,5, 1)),
    ("egduran@fiu.edu", "Graduate Applications Office",
     "Guidance for graduate applicants seeking industry roles", "Medium", datetime(2025,5, 1)),

    # ─ Yisell Cirion (Career Dev Programming) ─
    ("ycirion@fiu.edu",              "KFSCIS Seminar Series",
     "Aligns with guest-speaker seminar programming",           "High", datetime(2025,5, 1)),
    ("ycirion@fiu.edu",              "Workshops & Short Courses",
     "Coordinates professional-development offerings",         "High", datetime(2025,5, 1)),
    ("ycirion@fiu.edu",              "Break Through Tech Miami (BTT FIU)",
     "Integrates Data Corps & cohort programs",                 "Medium", datetime(2025,5, 1)),

    # ─ Darren Gregory (MBTI & Strong focus) ─
    ("dgregory@fiu.edu","Peer Tutoring (STARS & ASI)",
     "Supports student-skill fit & academic success",          "High", datetime(2025,5, 1)),
    ("dgregory@fiu.edu","Career & Talent Development",
     "Leverages career assessments in advising",                "Medium", datetime(2025,5, 1)),

    # ─ Audrey Johnson (Engineering Liaison) ─
    ("johnsona@fiu.edu","SOLID Lab",
     "Direct tie to cyber-physical research in computing",      "High", datetime(2025,5, 1)),
    ("johnsona@fiu.edu","CAESCIR",
     "Critical-infrastructure resilience collaborations",       "Medium", datetime(2025,5, 1)),
    ("johnsona@fiu.edu","Break Through Tech Miami (BTT FIU)",
     "Industry workshops for engineering cohorts",             "Low",  datetime(2025,5, 1)),

    # ─ Cristina Ebbage (Directed Pathways) ─
    ("cebbage@fiu.edu","Center for Diversity in Engineering & Computing",
     "Aligns with inclusive pathways initiatives",             "High", datetime(2025,5, 1)),
    ("cebbage@fiu.edu","Bioinformatics Research Group (BioRG)",
     "Supports interdisciplinary student cohorts",            "Medium", datetime(2025,5, 1)),
    ("cebbage@fiu.edu","Peer Tutoring (STARS & ASI)",
     "Reinforces pathway-based course support",               "Medium", datetime(2025,5, 1)),

    # ─ Dante Medina (Hospitality/Tourism) ─
    ("dmedina@fiu.edu","Career & Talent Development",
     "General career services for all majors",                 "High", datetime(2025,5, 1)),
    ("dmedina@fiu.edu","Graduate Applications Office",
     "Guidance for hospitality grad applicants",               "Medium", datetime(2025,5, 1)),
]

# ───────────────────────────────────────────────────────────────────────────
# 4) Build name→ID map for Additional_Opportunities
def fetch_opportunity_set(cur):
    cur.execute("SELECT opportunity_name FROM Additional_Opportunities")
    return {row[0] for row in cur.fetchall()}

# ───────────────────────────────────────────────────────────────────────────
# 5) Prepare rows for upsert and warn on missing names
def build_rows(op_set):
    rows, skipped = [], {}
    for email, opp_name, reason, prio, linked in ADVISOR_OPPORTUNITIES:
        if opp_name not in op_set:
            skipped.setdefault(opp_name, []).append(email or "<no-email>")
            continue
        rows.append((email, opp_name, reason, prio, linked))
    if skipped:
        for opp, emails in skipped.items():
            print(f"⚠️  '{opp}' not found (skipped for: {', '.join(emails)})")
    return rows

# ───────────────────────────────────────────────────────────────────────────
# 6) Upsert into Career_Advisor_Opportunity
SQL = """
INSERT INTO Career_Advisor_Opportunity
  (advisor_email, opportunity_name, recommendation_reason,
   priority_level, date_linked)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (advisor_email, opportunity_name) DO UPDATE
   SET recommendation_reason = EXCLUDED.recommendation_reason,
       priority_level        = EXCLUDED.priority_level,
       date_linked           = EXCLUDED.date_linked;
"""

def load_career_advisor_opportunity():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            op_set = fetch_opportunity_set(cur)
            rows   = build_rows(op_set)
            if rows:
                cur.executemany(SQL, rows)
                print(f"✅  Upserted {len(rows)} advisor–opportunity links.")
            else:
                print("ℹ️  Nothing to upsert.")
    finally:
        conn.close()
