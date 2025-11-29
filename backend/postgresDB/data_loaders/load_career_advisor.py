# load_career_advisor.py  –  manually‐curated loader for all CTD Career Advisor entries

import os, sys

# add parent dir so we can import db_config
script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from db_config import get_connection

# ────────────────────────────────────────────────────
# 1) CTD_ADVISORS: (full_name, title, email, phone, office, website,
#                  industry_specialty, affiliated_departments, graduate_undergrad)
# ────────────────────────────────────────────────────
CTD_ADVISORS = [
#  full_name,                     title,                                                        email,                 phone,          office,                               website,                                        industry_specialty,                                                  affiliated_departments,                       graduate_undergrad
    ("Ruth E. Pacheco",            "Executive Director, Industry Partnerships & Career Readiness", "rutpache@fiu.edu", "305-348-4866", "SASC 305, MMC",  "https://career.fiu.edu/administrative-team/#ruth-e-pacheco",           "Industry Partnerships & Career Readiness",                  "CTD; Center for Testing & Career Certification",       "UG/G"),
    ("Harold Clayton",             "Director, FIU Career Liaison Program & Campus Engagement",      "heclayto@fiu.edu","305-919-5770","WUC 253, BBC",  "https://career.fiu.edu/administrative-team/#harold-clayton",           "Campus Engagement & Liaison",                               "CTD",                                                    "UG/G"),
    ("Efigenia Gonzalez-Duran",    "Director, Employer Engagement & Support",                       "egduran@fiu.edu", "305-348-6189", "SASC 305, MMC",  "https://career.fiu.edu/administrative-team/#efigenia-gonzalez-duran", "Employer Engagement & Support",                             "CTD",                                                   "UG/G"),
    ("Yisell Cirion",              "Director, Career Development & Integrated Partnerships",        "ycirion@fiu.edu", "(305) 348-2423", "SASC 305, MMC",  "https://career.fiu.edu/administrative-team/#yisell-cirion",           "Career Development Programming",                          "CTD",                                                      "UG/G"),
    ("Darren Gregory",             "Career Specialist",                                            "dgregory@fiu.edu","305-348-2423","SASC 305, MMC",  "https://career.fiu.edu/career-development-team/#darren-gregory",          "MBTI & Strong Assessments; first-gen focus",              "CTD; Career Connections & Directed Pathways",           "UG"),
    ("Audrey Johnson",             "Career Specialist, College of Engineering & Computing",        "johnsona@fiu.edu","305-348-2423","SASC 305, MMC",  "https://career.fiu.edu/career-development-team/#audrey-johnson",          "Engineering & Computing career development",               "CTD; Liaison for KFSCIS",                               "UG/G"),
    ("Cristina Ebbage",            "Career Advisor, Career Connections & Directed Pathways",       "cebbage@fiu.edu","305-348-9893","SASC 305, MMC",  "https://career.fiu.edu/career-development-team/#cristina-ebbage",         "Directed Pathways & Program Alignment",                    "CTD; Career Connections & Directed Pathways",            "UG/G"),
    ("Dante Medina",               "Career Advisor, Hospitality & Tourism Management",             "dmedina@fiu.edu","305-348-6725","Wolfson School, BBC","https://career.fiu.edu/career-development-team/#dante-medina",       "Hospitality & Tourism career development",                 "CTD; Wolfson School of Hospitality & Tourism Management", "UG"),
    ("Claudia Romero",             "Career Advisor, Career Connections & Directed Pathways",       "cromero@fiu.edu","305-348-8015","SASC 305, MMC",  "https://career.fiu.edu/career-development-team/#claudia-romero",           "Industrial-Organizational Psychology & mental-health",    "CTD; Career Connections & Directed Pathways",            "UG/G"),
]

# ────────────────────────────────────────────────────
# 2) Re‐order into (advisor_email, full_name, title, office_location,
#                  phone_number, website, industry_specialty,
#                  affiliated_departments, graduate_undergrad)
# ────────────────────────────────────────────────────
ROWS = [
    (
        email,        # advisor_email
        full_name,    # full_name
        title,        # title
        office,       # office_location
        phone,        # phone_number
        website,      # website
        specialty,    # industry_specialty
        depts,        # affiliated_departments
        gradug        # graduate_undergrad
    )
    for full_name, title, email, phone, office, website, specialty, depts, gradug
    in CTD_ADVISORS
    # skip entries without email
    if email
]

# ────────────────────────────────────────────────────
# 3) Upsert into Career_Advisor
# ────────────────────────────────────────────────────
SQL = """
INSERT INTO Career_Advisor
  (advisor_email, full_name, title, office_location,
   phone_number, website, industry_specialty,
   affiliated_departments, graduate_undergrad)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (advisor_email) DO UPDATE
  SET full_name              = EXCLUDED.full_name,
      title                  = EXCLUDED.title,
      office_location        = EXCLUDED.office_location,
      phone_number           = EXCLUDED.phone_number,
      website                = EXCLUDED.website,
      industry_specialty     = EXCLUDED.industry_specialty,
      affiliated_departments = EXCLUDED.affiliated_departments,
      graduate_undergrad     = EXCLUDED.graduate_undergrad;
"""

def load_career_advisor():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            # clear out old records first
            cur.execute("DELETE FROM Career_Advisor;")
            # then bulk‐upsert
            cur.executemany(SQL, ROWS)
        print(f"✅  Upserted {len(ROWS)} career advisor records.")
    finally:
        conn.close()

