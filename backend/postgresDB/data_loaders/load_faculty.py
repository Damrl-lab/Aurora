# Manually-curated loader for all KFSCIS “Staff” entries
# Source: https://www.cis.fiu.edu/faculty-staff/ :contentReference[oaicite:0]{index=0}

import os, sys

# import of db_config.py from the parent directory
script_dir = os.path.dirname(__file__)              
parent_dir = os.path.dirname(script_dir)            
sys.path.append(parent_dir)
from db_config import get_connection

# fixed department for all staff
DEPARTMENT = "KFSCIS"

# ──────────────────────────────────────────────────────────────────
# 1) Fields: (full_name, title, email, phone, office, website)
# ──────────────────────────────────────────────────────────────────

STAFF = [
    ("S. S. Iyengar"         , "Ryder Professor and Director"                                                        , "iyengar@cis.fiu.edu"    , "305-348-3947" , "ECS 351"  , "https://www.cis.fiu.edu/faculty-staff/s-s-iyengar/"),            # :contentReference[oaicite:3]{index=3}
    ("Mark Allen Weiss"      , "Associate Director & Professor"                                                      , "weissma@cis.fiu.edu"    , "305-348-2036" , "ECS 353"  , "https://www.cis.fiu.edu/faculty-staff/mark-allen-weiss/"),      # :contentReference[oaicite:4]{index=4}
    ("Shu-Ching Chen"        , "Professor"                                                                           , "chens@cis.fiu.edu"      , "305-348-3480" , "ECS 362"  , "https://www.cis.fiu.edu/faculty-staff/shu-ching-chen/"),         # :contentReference[oaicite:5]{index=5}
    ("Xudong He"             , "Professor"                                                                           , "hex@cis.fiu.edu"        , "305-348-1831" , "ECS 212B", "https://www.cis.fiu.edu/faculty-staff/xudong-he/"),          # :contentReference[oaicite:6]{index=6}
    ("Giri Narasimhan"       , "Professor & Assoc. Dean for Research and Graduate Studies"                           , "gnarasim@cis.fiu.edu"   , "305-348-3748" , "ECS 254"  , "https://www.cis.fiu.edu/faculty-staff/giri-narasimhan/"),     # :contentReference[oaicite:7]{index=7}
    ("Jainendra K Navlakha"  , "Professor"                                                                           , "jnavlakha@cis.fiu.edu"  , "305-348-2026" , "ECS 384"  , "https://www.cis.fiu.edu/faculty-staff/jainendra-k-navlakha/"),  # :contentReference[oaicite:8]{index=8}
    ("Niki Pissinou"         , "Professor"                                                                           , "npissino@cis.fiu.edu"   , "305-348-3716" , "EC 2914"   , "https://www.cis.fiu.edu/faculty-staff/niki-pissinou/"),         # :contentReference[oaicite:9]{index=9}
    ("Naphtali Rishe"        , "Professor"                                                                           , "rrishe@cis.fiu.edu"     , "305-348-2025" , "ECS 243"  , "https://www.cis.fiu.edu/faculty-staff/naphtali-rishe/"),        # :contentReference[oaicite:10]{index=10}
    ("Peter J Clarke"        , "Associate Professor"                                                                 , "clarkep@cis.fiu.edu"    , "305-348-2440" , "ECS 212A", "https://www.cis.fiu.edu/faculty-staff/peter-j-clarke/"),    # :contentReference[oaicite:11]{index=11}
    ("Tao Li"                , "Associate Professor"                                                                 , "taoli@cis.fiu.edu"      , "305-348-6036" , "ECS 318"  , "https://www.cis.fiu.edu/faculty-staff/tao-li/"),               # :contentReference[oaicite:12]{index=12}
    ("Christine Lisetti"     , "Associate Professor"                                                                 , "clisetti@cis.fiu.edu"   , "305-348-6242" , "ECS 361"  , "https://www.cis.fiu.edu/faculty-staff/christine-lisetti/"),    # :contentReference[oaicite:13]{index=13}
    ("Jason Liu"             , "Associate Professor"                                                                 , "jliu8@cis.fiu.edu"      , "305-348-1625" , "ECS 261B", "https://www.cis.fiu.edu/faculty-staff/jason-liu/"),         # :contentReference[oaicite:14]{index=14}
    ("Masoud Milani"         , "Associate Professor & Director, Office of Student Access & Success / Ctr. for Diversity in Engr. and Computing"
                             , "mmilani@cis.fiu.edu"    , "305-348-2925" , "ECS 388"  , "https://www.cis.fiu.edu/faculty-staff/masoud-milani/"),        # :contentReference[oaicite:15]{index=15}
    ("Alex Pelin"            , "Associate Professor"                                                                 , "apelin@cis.fiu.edu"     , "305-348-3386" , "ECS 383"  , "https://www.cis.fiu.edu/faculty-staff/alex-pelin/"),         # :contentReference[oaicite:16]{index=16}
    ("Nagarajan Prabakar"    , "Associate Professor"                                                                 , "nprabaka@cis.fiu.edu"   , "305-348-2033" , "ECS 382"  , "https://www.cis.fiu.edu/faculty-staff/nagarajan-prabakar/"),  # :contentReference[oaicite:17]{index=17}
    ("Raju Rangaswami"       , "Associate Professor"                                                                 , "raju@cis.fiu.edu"       , "305-348-6230" , "ECS 386"  , "https://www.cis.fiu.edu/faculty-staff/raju-rangaswami/"),     # :contentReference[oaicite:18]{index=18}
    ("S. Masoud Sadjadi"     , "Associate Professor"                                                                 , "sadjadi@cis.fiu.edu"    , "305-348-1835" , "ECS 212C", "https://www.cis.fiu.edu/faculty-staff/s-masoud-sadjadi/"),# :contentReference[oaicite:19]{index=19}
    ("Geoffrey Smith"        , "Associate Professor"                                                                 , "geoffrey.smith@cis.fiu.edu", "305-348-6037", "ECS 320", "https://www.cis.fiu.edu/faculty-staff/geoffrey-smith/"), # :contentReference[oaicite:20]{index=20}
    ("Bogdan Carbunar"       , "Assistant Professor"                                                                 , "bc@cis.fiu.edu"         , "305-348-7566" , "ECS 310"  , "https://www.cis.fiu.edu/faculty-staff/bogdan-carbunar/"),    # :contentReference[oaicite:21]{index=21}
    ("Radu Jianu"            , "Assistant Professor"                                                                 , "rjianu@cis.fiu.edu"     , "305-348-1614" , "ECS 314"  , "https://www.cis.fiu.edu/faculty-staff/radu-jianu/"),         # :contentReference[oaicite:22]{index=22}
    ("Deng Pan"              , "Assistant Professor"                                                                 , "dpan@cis.fiu.edu"       , "305-348-7567" , "ECS 261A", "https://www.cis.fiu.edu/faculty-staff/deng-pan/"),         # :contentReference[oaicite:23]{index=23}
    ("Shaolei Ren"           , "Assistant Professor"                                                                 , "sren@cis.fiu.edu"       , "305-348-2032" , "ECS 350"  , "https://www.cis.fiu.edu/faculty-staff/shaolei-ren/"),        # :contentReference[oaicite:24]{index=24}
    ("Xin Sun"               , "Assistant Professor"                                                                 , "xsun@cis.fiu.edu"       , "305-348-3987" , "ECS 381"  , "https://www.cis.fiu.edu/faculty-staff/xin-sun/"),          # :contentReference[oaicite:25]{index=25}
    ("Jinpeng Wei"           , "Assistant Professor"                                                                 , "jwei@cis.fiu.edu"       , "305-348-4038" , "ECS 389"  , "https://www.cis.fiu.edu/faculty-staff/jinpeng-wei/"),        # :contentReference[oaicite:26]{index=26}
    ("Ning Xie"              , "Assistant Professor"                                                                 , "nxie@cis.fiu.edu"       , "305-348-2015" , "ECS 380"  , "https://www.cis.fiu.edu/faculty-staff/ning-xie/"),         # :contentReference[oaicite:27]{index=27}
    ("Wei Zeng"              , "Assistant Professor"                                                                 , "wzeng@cis.fiu.edu"      , "305-348-2019" , "ECS 357"  , "https://www.cis.fiu.edu/faculty-staff/wei-zeng/"),          # :contentReference[oaicite:28]{index=28}
    ("Ming Zhao"             , "Assistant Professor"                                                                 , "mzhao@cis.fiu.edu"      , "305-348-2034" , "ECS 363"  , "https://www.cis.fiu.edu/faculty-staff/ming-zhao/"),         # :contentReference[oaicite:29]{index=29}
    ("Jong-Hoon Kim"         , "Visiting Assistant Professor"                                                        , "jkim@cis.fiu.edu"       , "305-348-3751" , "ECS 231"  , "https://www.cis.fiu.edu/faculty-staff/jong-hoon-kim/"),   # :contentReference[oaicite:30]{index=30}
    ("Tim Downey"            , "Senior Instructor"                                                                   , "timothy.downey@cis.fiu.edu", "305-348-3329","ECS 316", "https://www.cis.fiu.edu/faculty-staff/tim-downey/"),  # :contentReference[oaicite:31]{index=31}
    ("Kip Irvine"            , "Senior Instructor"                                                                   , "kip@cis.fiu.edu"        , "305-348-1528" , "ECS 360"  , "https://www.cis.fiu.edu/faculty-staff/kip-irvine/"),         # :contentReference[oaicite:32]{index=32}
    ("Norman D Pestaina"     , "Senior Instructor"                                                                   , "npestain@cis.fiu.edu"   , "305-348-2013" , "ECS 364"  , "https://www.cis.fiu.edu/faculty-staff/norman-d-pestaina/"),# :contentReference[oaicite:33]{index=33}
    ("Greg Shaw"             , "Senior Instructor"                                                                   , "gshaw@cis.fiu.edu"      , "305-348-1550" , "ECS 313"  , "https://www.cis.fiu.edu/faculty-staff/greg-shaw/"),          # :contentReference[oaicite:34]{index=34}
    ("Jill Weiss"            , "Senior Instructor"                                                                   , "jweiss@cis.fiu.edu"     , "305-348-1545" , "ECS 385"  , "https://www.cis.fiu.edu/faculty-staff/jill-weiss/"),         # :contentReference[oaicite:35]{index=35}
    ("Walid Akache"          , "Instructor"                                                                          , "wakache@cis.fiu.edu"    , "305-348-3731" , "ECS 312"  , "https://www.cis.fiu.edu/faculty-staff/walid-akache/"),      # :contentReference[oaicite:36]{index=36}
    ("Joslyn Smith"          , "Instructor"                                                                          , "joslyns@cis.fiu.edu"    , "305-348-2015" , "ECS 365"  , "https://www.cis.fiu.edu/faculty-staff/joslyn-smith/"),       # :contentReference[oaicite:37]{index=37}
    ("Toby S Berk"           , "Professor Emeritus"                                                                  , None                     , "305-348-2744" , None       , None),                                             # :contentReference[oaicite:38]{index=38}
    ("Bill Kraynek"          , "Professor Emeritus"                                                                  , "bkraynek@cis.fiu.edu"   , "305-348-2744" , "ECS 384"  , "https://www.cis.fiu.edu/faculty-staff/bill-kraynek/"),      # :contentReference[oaicite:39]{index=39}
    ("Patricia McDermott-Wells", "Visiting Instructor"                                                              , "pmcdermott@cis.fiu.edu", "305-348-2844" , "ECS 365"  , "https://www.cis.fiu.edu/faculty-staff/patricia-mcdermott-wells/"),  # :contentReference[oaicite:40]{index=40}
    ("Trevor Cickovski"      , "Associate Director & Associate Teaching Professor"                                   , "tcickovs@fiu.edu"       , "305-348-8043", "CASE 344A", "http://cis.fiu.edu/~tcickovs"),  # :contentReference[oaicite:0]{index=41}
    ("Janki Bhimani"        , "Assistant Professor"                                                                 , "jbhimani@fiu.edu"        , "305-348-9934", "CASE 238B", "https://damrl.cs.fiu.edu/janki-bhimani/#cv"),  # :contentReference[oaicite:1]{index=42
]


# ──────────────────────────────────────────────────────────────────
# 2) Transform into DB rows
rows = [
    (
        email,
        name,
        DEPARTMENT,
        title,
        office,
        phone,
        site
    )
    for name, title, email, phone, office, site in STAFF
    if email
]

# ──────────────────────────────────────────────────────────────────
# 3) Upsert into Faculty
SQL = """
INSERT INTO Faculty
 (faculty_email, full_name, department, title,
  office_location, phone_number, website)
VALUES (%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (faculty_email) DO UPDATE
  SET full_name       = EXCLUDED.full_name,
      department      = EXCLUDED.department,
      title           = EXCLUDED.title,
      office_location = EXCLUDED.office_location,
      phone_number    = EXCLUDED.phone_number,
      website         = EXCLUDED.website;
"""

def load_faculty():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(SQL, rows)
        print(f"✅  Upserted {len(rows)} staff records.")
    finally:
        conn.close()
