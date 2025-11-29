import os
import sys

# import of db_config.py from the parent directory
script_dir = os.path.dirname(__file__)              
parent_dir = os.path.dirname(script_dir)            
sys.path.append(parent_dir)
from db_config import get_connection

# ───────────────────────────────────────────────────────────────────
# 1.  FULL CATALOGUE
#     (program_id) -> list[ tuple(course_id, is_core, recommended_year) ]
# ───────────────────────────────────────────────────────────────────
CATALOG: dict[str, list[tuple[str, bool, int | None]]] = {

    # ========  Undergraduate  =================================================
    "CS-BA": [  
        # Year 1
        ("CGS_1920", True, 1), ("MAC_1147", True, 1),               # Pre‑Calc
        ("COP_1000", True, 1), ("IDC_1000", False, 1),              # choose‑one intro
        ("MAD_2104", True, 1), ("COT_3100", True, 1),
        # Year 2
        ("STA_2023", True, 2), ("COP_2210", True, 2),
        ("COP_3337", True, 2), ("COP_3530", True, 2),
        # Year 3
        ("ENC_3249", True, 3), ("CGS_3095", True, 3),
        ("CDA_3102", True, 3), ("COP_4338", True, 3),
        # Year 4
        ("CEN_4010", True, 4), ("COP_4610", True, 4),
        # Capstone & interdisciplinary credits (handled outside SCIS)
        ("CIS_3950", True, 4), ("CIS_4951", True, 4),
        # Elective groups   (6 courses, pick ≥1 from each block)
        ("COP_4534", False, 3), ("COP_4555", False, 3),
        ("COT_3541", False, 3), ("CAP_4630", False, 4),
        ("CNT_4713", False, 4), ("CEN_4021", False, 4),
        ("CEN_4072", False, 4), ("COP_4710", False, 4),
        ("CAP_4770", False, 4), ("COT_4431", False, 4),
    ],

    "CS-BS": [
        # core
        ("CGS_1920",  True, 1),     ("MAC_2311",  True, 1),
        ("MAC_2312",  True, 1),     ("COP_2210",  True, 2),
        ("MAD_2104",  True, 2),     ("COT_3100",  True, 2),
        ("STA_3033",  True, 3),     ("CDA_3102",  True, 3),
        ("COP_3337",  True, 3),     ("COP_3530",  True, 3),
        ("CDA_4101",  True, 4),     ("CGS_3095",  True, 3),
        ("CEN_4010",  True, 4),     ("CNT_4713",  True, 4),
        ("COP_4555",  True, 4),     ("COP_4610",  True, 4),
        ("COP_4710",  True, 4),     ("MAD_3512",  True, 3),
        ("CIS_3950",  True, 3),     ("CIS_4951",  True, 4),
        ("ENC_3249",  True, 3),
        # electives pool
        # Foundations
        ("COP_4534", False, 3),     ("COT_3541", False, 3),
        ("COT_4521", False, 3),     ("MAD_3301", False, 3),
        ("MAD_3401", False, 3),     ("MAD_4203", False, 3),
        ("MHF_4302", False, 3),     
        #  – Systems
        ("CAP_4453", False, 3),
        ("CDA_4625", False, 3),
        ("CEN_4083", False, 3),
        ("COP_4520", False, 3),
        ("COP_4604", False, 4),
        ("COP_4751", False, 4),
        ("CTS_4408", False, 4),
        ("COT_4431", False, 4),
         #  – Applications
        ("CAP_4104", False, 3),
        ("CAP_4630", False, 3),
        ("CAP_4641", False, 3),
        ("CAP_4710", False, 3),
        ("CAP_4770", False, 3),
        ("CAP_4612", False, 3),
        ("CAP_4506", False, 3),
        ("COP_4226", False, 3),
        ("CEN_4021", False, 4),
        ("CEN_4072", False, 4),
        ("CIS_4731", False, 4),
        ("CAP_4052", False, 4),
        ("CAP_4830", False, 4),
        ("COT_4601", False, 4),
    ],

    "CS-BS-SDD": [
         # identical first‑two years to CS‑BS
        ("CGS_1920",  True, 1),
        ("MAC_2311",  True, 1),
        ("MAC_2312",  True, 1),
        ("COP_2210",  True, 2),
        ("MAD_2104",  True, 2),
        ("COT_3100",  True, 2),
        ("CDA_3102",  True, 3),
        ("COP_3337",  True, 3),
        ("COP_3530",  True, 3),
        ("CGS_3095",  True, 3),
        ("CEN_4010",  True, 3),
        ("STA_3033",  True, 3),
        # specialised core in SDD
        ("COP_4610",  True, 4),
        ("CEN_4021",  True, 4),
        ("CEN_4072",  True, 4),
        ("CNT_4713",  True, 4),
        ("CIS_3950",  True, 4),
        ("CIS_4951",  True, 4),
        ("ENC_3249",  True, 3),
        # SDD has **5** electives – at least one Foundations & one Systems
        # Foundations
        ("COP_4534", False, 3),
        ("COT_3541", False, 3),
        ("COT_4521", False, 3),
        # Systems
        ("CAP_4453", False, 3),
        ("CDA_4625", False, 3),
        ("CEN_4083", False, 3),
        ("COP_4520", False, 3),
        ("COP_4604", False, 4),
        ("COP_4710", False, 4),
        ("COP_4751", False, 4),
        ("COT_4431", False, 4),
        # Applications (optional pool)
        ("CAP_4104", False, 3),
        ("CAP_4506", False, 3),
        ("CAP_4630", False, 3),
        ("CAP_4641", False, 3),
        ("CAP_4710", False, 3),
        ("CAP_4770", False, 3),
        ("CAP_4612", False, 3),
        ("COP_4226", False, 3),
        ("CIS_4731", False, 4),
        ("CAP_4052", False, 4),
        ("CAP_4830", False, 4),
        ("COT_4601", False, 4),
        ("CTS_4408", False, 4),
    ],

    "CS-MINOR": [
        ("MAC_1147", True, None),
        ("COP_2210", True, None), ("COP_3337", True, None),
        ("MAD_2104", True, None), ("COT_3100", True, None),
        ("COP_3530", True, None), ("CDA_3102", True, None),
        # choose 2 electives
        ("COP_4534", False, None), ("COP_4555", False, None),
        ("CEN_4021", False, None), ("CAP_4630", False, None),
        ("COP_4710", False, None), ("COT_4431", False, None),
    ],

    "DS-BS": [
        # Year 1
        ("MAC_2311", True, 1), ("MAC_2312", True, 1),
        ("CTS_1500", True, 1), ("CAP_2757", True, 1),
        ("COP_2047", True, 1),
        # Year 2
        ("MAD_2104", True, 2), ("COT_3100", True, 2),
        ("COP_3410", True, 2), ("STA_2023", True, 2),
        ("STA_3111", True, 2),
        # Year 3
        ("STA_4321", True, 3), ("STA_4853", True, 3),
        ("CAP_4612", True, 3), ("CAP_5610", True, 3),
        ("COP_5725", True, 3),
        # Year 4
        ("IDC_4323", True, 4), ("CIS_3950", True, 4), ("CIS_4951", True, 4),
        # Natural‑science lab track
        ("BSC_2010", True, 2), ("BSC_2010L", True, 2),
        ("PHY_2048", True, 2), ("PHY_2048L", True, 2),
        # Concentration electives (12 cr) – representative list
        ("CAP_4630", False, 4), ("CAP_4770", False, 4),
        ("CAI_4203", False, 4), ("CEN_4083", False, 4),
        ("COP_4534", False, 3), ("COT_4431", False, 3),
        ("CAP_4830", False, 4), ("STA_3163", False, 3), ("STA_3164", False, 4),
    ],

    "IT-BA": [
        # Year 1‑2 core
        ("COP_2250", True, 1), ("MAD_1100", True, 1),
        ("COT_3100", True, 2),
        # Programming sequence
        ("COP_3804", True, 2),
        # Year 3‑4 track
        ("CEN_3721", True, 3), ("CGS_3767", True, 3),
        ("CGS_4285", True, 3),
        ("CTE_4600", True, 4),
        ("CIS_3950", True, 4), ("CIS_4951", True, 4),
        # IT electives (12 cr) – sample
        ("CGS_4854", False, 3), ("COP_4703", False, 3),
        ("CNT_4403", False, 3), ("CTS_4408", False, 3),
        ("COP_4751", False, 4), ("CIS_4365", False, 4),
        ("CNT_4513", False, 4), ("COP_4655", False, 4),
    ],

    "IT-BS": [
        ("CGS_1920", True, 1), ("MAD_1100", True, 1),
        ("COP_2250", True, 1), ("COT_3100", True, 2),
        ("CGS_3095", True, 2), ("COP_3804", True, 2),
        ("CEN_3721", True, 3),
        ("CGS_3767", True, 3), ("CGS_4285", True, 3),
        ("ENC_3249", True, 3),
        ("CNT_4403", True, 3), ("COP_4814", True, 3),
        ("CGS_4854", True, 3),
        ("COP_4703", True, 3), ("CIS_3950", True, 4),
        ("CIS_4951", True, 4),
        # Five electives (App Dev & Systems/Network pools) – subset
        ("COP_4751", False, 4), ("CTS_4408", False, 4),
        ("CNT_4513", False, 4), ("CNT_4504", False, 4),
        ("CIS_4431", False, 4), ("CTS_4348", False, 4),
        ("COP_4655", False, 4), ("CNT_4603", False, 4),
    ],

    "IT-BS-SW": [
        ("CGS_1920", True, 1), ("MAD_2104", True, 1),
        ("COP_2210", True, 1), ("COT_3100", True, 2),
        ("CGS_3095", True, 2), ("COP_3337", True, 2),
        ("CEN_3721", True, 3), ("COP_3530", True, 3),
        ("COP_4338", True, 3), ("CDA_3102", True, 3),
        ("ENC_3249", True, 3),
        ("COP_4814", True, 3), ("COP_4703", True, 3),
        ("COP_4751", False, 4), ("CAP_4601", False, 4),
        ("COP_4655", False, 4), ("COP_4005", False, 4),
        ("CIS_3950", True, 4), ("CIS_4951", True, 4),
    ],

    # ========  Graduate  ===========================================
    "MS-CS": [
         # ‑‑‑ REQUIRED CORE (9 cr) ‑‑‑
        ("COT_5407", True, 1),   # Intro‑to‑Algorithms
        ("CEN_5011", True, 1),   # students pick 2 of the next 3 …
        ("COP_5614", True, 1),
        ("COP_5725", True, 1),
         # ‑‑‑ ELECTIVE POOL (pick 5–7) – mark as electives, year 2.
        # (list comes from first PDF page)
        ("CAP_5011", False, 2), ("CAP_5109", False, 2),
        ("CAP_5507", False, 2), ("CAP_5510C",False, 2),
        ("CAP_5602", False, 2), ("CAP_5610", False, 2),
        ("CAP_5627", False, 2), ("CAP_5640", False, 2),
        ("CAP_5701", False, 2), ("CAP_5738", False, 2),
        ("CAP_5768", False, 2), ("CAP_5771", False, 2),
        ("CAP_6736", False, 2), ("CAP_6776", False, 2),
        ("CAP_6778", False, 2), ("CDA_5655", False, 2),
        ("CDA_6939", False, 2), ("CEN_5064", False, 2),
        ("CEN_5076", False, 2), ("CEN_5079", False, 2),
        ("CEN_5082", False, 2), ("CEN_5120", False, 2),
        ("CEN_6070", False, 2), ("CEN_6075", False, 2),
        ("CIS_5208", False, 2), ("CIS_5346", False, 2),
        ("CIS_5370", False, 2), ("CIS_5372", False, 2),
        ("CIS_5373", False, 2), ("CIS_5374", False, 2),
        ("CIS_5432", False, 2), ("CIS_5931", False, 2),
        ("CIS_6612", False, 2), ("CIS_6930", False, 2),
        ("CNT_5109", False, 2), ("CNT_5415", False, 2),
        ("CNT_6207", False, 2), ("CNT_6208", False, 2),
        ("COP_5621", False, 2), ("COP_6556", False, 2),
        ("COP_6611", False, 2), ("COP_6727", False, 2),
        ("COP_6795", False, 2), ("COT_5310", False, 2),
        ("COT_5428", False, 2), ("COT_5520", False, 2),
        ("COT_6421", False, 2), ("COT_6446", False, 2),
        ("COT_6930", False, 2), ("COT_6931", False, 2),
        ("COT_6936", False, 2), ("TCN_5010", False, 2),
        ("TCN_5030", False, 2), ("TCN_5060", False, 2),
        ("TCN_5080", False, 2), ("TCN_5150", False, 2),
        ("TCN_5421", False, 2), ("TCN_5440", False, 2),
        ("TCN_5445", False, 2), ("TCN_5640", False, 2),
        ("TCN_5710", False, 2), ("TCN_6210", False, 2),
        ("TCN_6215", False, 2), ("TCN_6230", False, 2),
        ("TCN_6260", False, 2), ("TCN_6270", False, 2),
        ("TCN_6275", False, 2), ("TCN_6420", False, 2),
        ("TCN_6430", False, 2), ("TCN_6450", False, 2),
        ("TCN_6880", False, 2),
    ],

    "MS-DS": [
        # ‑‑‑ REQUIRED CORE (12 cr) ‑‑‑
        ("CAP_5602", True, 1),
        ("CAP_5768", True, 1),
        ("CAP_5771", True, 1),           # or COP_5577 (not in list)
        ("STA_6244", True, 1),           # may swap for track‑specific

        # ‑‑‑ CAPSTONE (3 cr) – still core
        ("IDC_6940", True, 2),

        # electives are track‑specific; mark them as electives year 2
        # • Artificial Intelligence track
        ("CAP_5109", False, 2), ("CAP_5507", False, 2),
        ("CAP_5510C",False, 2), ("CAP_5627", False, 2),
        ("CAP_5640", False, 2), ("CAP_5610", False, 2),
        ("CAP_6619", False, 2), ("CEN_5120", False, 2),
        ("EEL_5820", False, 2), ("EEL_5813", False, 2),
        ("STA_6247", False, 2),

        # • Computational Data Analytics (partial list)
        ("CAP_5738", False, 2), ("CAP_6776", False, 2),
        ("CAP_6778", False, 2), ("CEN_5082", False, 2),
        ("CIS_5372", False, 2), ("CIS_5374", False, 2),
        ("COP_5725", False, 2), ("COP_6727", False, 2),
        ("COT_6405", False, 2),

    ],

    "PHD-CS": [
        # core curriculum (B or better)
        ("COP_5614", True, 1),
        ("COT_5310", True, 1),
        ("COT_6405", True, 1),

        # research & dissertation credit placeholders
        ("CIS_7910", False, None),   # graduate research (variable cr)
        ("CIS_7980", False, None),   # dissertation

        # elective pool (same list as MS‑CS, year 2+)
        ("CAP_5011", False, 2), ("CAP_5109", False, 2),
        ("CAP_5507", False, 2), ("CAP_5510C",False, 2),
        ("CAP_5602", False, 2), ("CAP_5610", False, 2),
        ("CAP_5627", False, 2), ("CAP_5640", False, 2),
        ("CAP_5701", False, 2), ("CAP_5738", False, 2),
        # … (same elective list as MS‑CS) …
    ],
}

# ───────────────────────────────────────────────────────────────────
# 2.  Helper functions
# ───────────────────────────────────────────────────────────────────
def _known_courses(cur) -> set[str]:
    cur.execute("SELECT course_id FROM Courses")
    return {row[0] for row in cur.fetchall()}

UPSERT_SQL = """
INSERT INTO Program_Course
  (program_id, course_id, is_core, recommended_year)
VALUES (%s,%s,%s,%s)
ON CONFLICT (program_id, course_id) DO UPDATE
  SET is_core          = EXCLUDED.is_core,
      recommended_year = EXCLUDED.recommended_year;
"""

# ───────────────────────────────────────────────────────────────────
# 3.  Main loader
# ───────────────────────────────────────────────────────────────────
def load_program_course():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            existing = _known_courses(cur)

            rows, skipped = [], {}
            for prog, lst in CATALOG.items():
                for course_id, is_core, year in lst:
                    if course_id not in existing:
                        skipped.setdefault(prog, []).append(course_id)
                        continue
                    rows.append((prog, course_id, is_core, year))

            if skipped:
                for prog, ids in skipped.items():
                    print(f"⚠️  {prog}: {len(ids)} unknown course_id(s) skipped "
                          f"(add them to Courses first): {', '.join(ids)}")

            if rows:
                cur.executemany(UPSERT_SQL, rows)
        print(f"✅  Upserted {len(rows)} rows into Program_Course.")
    finally:
        conn.close()
