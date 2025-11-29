import os, sys

# add parent dir so we can import db_config
script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from db_config import get_connection

# ───────────────────────────────────────────────────────────────────────────
# 1) Fields: (advisor_email, full_name, title,
#             graduate_undergrad, office_location, phone_number, website)
# ───────────────────────────────────────────────────────────────────────────

ACADEMIC_ADVISORS = [
    # direct individuals
    ("mcarr016@fiu.edu",  "Melanie Carrillo",  "Academic Advisor",             "UG", "PG6 101C", "305-348-7936", "https://www.cis.fiu.edu/faculty-staff/melanie-carrillo/"),
    ("abonny@fiu.edu",    "Ava Bonny",         "Academic Advisor",             "UG", "PG6 101B", "305-348-7936", "https://www.cis.fiu.edu/faculty-staff/ava-bonny/"),
    ("cpagan@fiu.edu",    "Carla Pagan",       "Academic Advisor",             "UG", "PG6 101D", "305-348-7936", "https://www.cis.fiu.edu/people/carla-pagan/"),
    ("jnaranjo@fiu.edu",  "Joselyn Naranjo",   "Director of Academic Advising","UG", "PG6 101A", "305-348-7936", "https://www.cis.fiu.edu/faculty-staff/joselyn-naranjo/"),
    ("rsuarez@cis.fiu.edu","Ruth Suarez",       "Manager of Academic Advising", "UG", "PG6 101J", "305-348-2022", "https://www.cis.fiu.edu/faculty-staff/ruth-suarez/"),
    ("knunez@fiu.edu",    "Karem Nunez",       "Academic Advisor",             "UG", "PG6 101C", "305-348-5074", "https://www.cis.fiu.edu/faculty-staff/karem-nunez/"),
    ("Lmorency@cis.fiu.edu", "Lauren Morency",    "Academic Advisor",             "UG", "PG6 101A", "305-348-5180", "https://www.cis.fiu.edu/faculty-staff/lauren-morency/"),
    ("fmoscoso@fiu.edu",    "Federico Moscoso L",   "Academic Advisor",         "UG",   "PG-6 Room 101 I",  "305-348-3744", "https://www.cis.fiu.edu/faculty-staff/federico-moscoso-l/"),
    ("cpagan@fiu.edu",      "Carla Pagan",      "Academic Advisor",             "UG",    "PG-6 101H",       "305-348-6382", "https://www.cis.fiu.edu/faculty-staff/carla-pagan/"),
    ("rarocha@fiu.edu",   "Rebeca Arocha",     "Graduate Program Advisor",     "G",  "CASE 350", "305-348-7989", "https://www.cis.fiu.edu/faculty-staff/rebeca-arocha/"),
]

# ───────────────────────────────────────────────────────────────────────────
# 2) Transform into DB rows
rows = [
    (
        email,
        name,
        title,
        gradug,
        office,
        phone,
        site
    )
    for (email, name, title, gradug, office, phone, site) in ACADEMIC_ADVISORS
    if email  # skip any truly blank emails
]

# ───────────────────────────────────────────────────────────────────────────
# 3) Upsert into Academic_Advisor
SQL = """
INSERT INTO Academic_Advisor
  (advisor_email, full_name, title,
   graduate_undergrad, office_location,
   phone_number, website)
VALUES (%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (advisor_email) DO UPDATE
  SET full_name          = EXCLUDED.full_name,
      title              = EXCLUDED.title,
      graduate_undergrad = EXCLUDED.graduate_undergrad,
      office_location    = EXCLUDED.office_location,
      phone_number       = EXCLUDED.phone_number,
      website            = EXCLUDED.website;
"""

def load_academic_advisor():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(SQL, rows)
        print(f"✅  Upserted {len(rows)} academic advisor records.")
    finally:
        conn.close()

