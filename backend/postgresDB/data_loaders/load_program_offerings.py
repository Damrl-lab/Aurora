import os, sys
from datetime import date

# import of db_config.py from the parent directory
script_dir = os.path.dirname(__file__)              
parent_dir = os.path.dirname(script_dir)            
sys.path.append(parent_dir)
from db_config import get_connection


ROWS = [
    # program_id, major_id, degree_level, prerequisites, description,
    # program_url, is_active, program_name, effective_since
    (
        "CS-BA", "CS", "BA",
        "COP2210, MAC1140+; COT3100 (coreq COP2210/COP2250/EEL2280); "
        "ENC UCC English; MAD2104." ,
        "SACS-accredited liberal-arts Computer Science degree (non-ABET).",
        "https://www.cis.fiu.edu/degree/b-a-computer-science/",
        True,
        "Bachelor of Arts in Computer Science",
        date(2022, 1, 1),
    ),
    (
        "CS-BS", "CS", "BS",
        "Same as CS-BA plus MAC2311; KF-SCIS approved science w/ lab.",
        "ABET-accredited CS track for students planning graduate study.",
        "https://www.cis.fiu.edu/degree/b-s-in-computer-science/",
        True,
        "Bachelor of Science in Computer Science – CS Track",
        date(2023, 8, 1),
    ),
    (
        "CS-BS-SDD", "CS", "BS",
        "Identical to CS-BS prerequisites; emphasis on software engineering.",
        "Software Design & Development track for software engineering careers.",
        "https://www.cis.fiu.edu/degree/software-design-and-development-track/",
        True,
        "Bachelor of Science in Computer Science – Software Design & Development",
        date(2023, 8, 1),
    ),
    (
        "CS-MINOR", "CS", "MINOR",
        "COP2210, COT3100, MAD2104 (plus coreqs as above).",
        "18-credit minor providing CS fundamentals for non-CS majors.",
        "https://www.cis.fiu.edu/degree/minor-in-computer-science/",
        True,
        "Minor in Computer Science",
        date(2023, 8, 1),
    ),
    (
        "DS-BS", "DS", "BS",
        "High-school algebra; completion of UCC English.",
        "Inter-disciplinary Data Science & AI degree blending CS, math, stats.",
        "https://www.cis.fiu.edu/degree/bs-data-science-and-ai/",
        True,
        "Bachelor of Science in Data Science and Artificial Intelligence",
        date(2024, 8, 1),
    ),
    (
        "IT-BA", "IT", "BA",
        "Completion of UCC English; second-major only.",
        "Flexible B.A. in IT for students pursuing a second bachelor’s degree.",
        "https://www.cis.fiu.edu/degree/second-major-in-information-technology-ba/",
        True,
        "Bachelor of Arts in Information Technology (2nd Major)",
        date(2010, 8, 1),
    ),
    (
        "IT-BS", "IT", "BS",
        "Completion of UCC English requirements.",
        "Core IT track covering networking, OS, web, security, HCI.",
        "https://www.cis.fiu.edu/degree/information-technology-track/",
        True,
        "Bachelor of Science in Information Technology – IT Track",
        date(2023, 8, 1),
    ),
    (
        "IT-BS-SW", "IT", "BS",
        "Completion of UCC English requirements.",
        "Software-oriented IT track (programming, SE, advanced web).",
        "https://www.cis.fiu.edu/degree/information-technology-track/",
        True,
        "Bachelor of Science in Information Technology – Software Track",
        date(2023, 8, 1),
    ),
    (
        "MS-CS", "CS", "MS",
        "≥ 75 CS BS credits with GPA ≥ 3.3.",
        "Research-focused master’s covering advanced CS topics.",
        "https://www.cis.fiu.edu/degree/master-of-science-in-computer-science/",
        True,
        "Master of Science in Computer Science",
        date(2020, 8, 1),
    ),
    (
        "MS-DS", "DS", "MS",
        "Acceptable bachelor’s; ≥ 75 credits; GPA ≥ 3.3.",
        "Graduate program in Data Science & AI with multiple tracks.",
        "https://www.cis.fiu.edu/degree/master-of-science-in-data-science/",
        True,
        "Master of Science in Data Science & Artificial Intelligence",
        date(2020, 8, 1),
    ),
    (
        "PHD-CS", "CS", "PHD",
        "CS/CE BS; GPA ≥ 3.2 last 60 hrs or 3.0 + MS (≥ 3.3); GRE waived through ’23.",
        "Doctoral research degree in CS (funding + qualifying exam required).",
        "https://www.cis.fiu.edu/degree/doctor-of-philosophy-in-computer-science/",
        True,
        "Doctor of Philosophy in Computer Science",
        date(2020, 8, 1),
    ),
     (
        "PM-CERT",                            
        "PM",                                 
        "CERT",                               
        None,                                 
        "Acquire the practical and strategic skills you need to become a product manager and supercharge your career in just 10 weeks.",  # description :contentReference[oaicite:1]{index=1}
        "https://business.fiu.edu/academics/executive-education/comprehensive-project-management-certificate-program/",  
        True,                                 
        "Product Management Certificate", 
        date(2025, 5, 5),                    
    ),
]

SQL = """
INSERT INTO Program_Offerings
    (program_id, major_id, degree_level, prerequisites,
     description, program_url, is_active, program_name, effective_since)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (program_id) DO UPDATE
  SET major_id        = EXCLUDED.major_id,
      degree_level    = EXCLUDED.degree_level,
      prerequisites   = EXCLUDED.prerequisites,
      description     = EXCLUDED.description,
      program_url     = EXCLUDED.program_url,
      is_active       = EXCLUDED.is_active,
      program_name    = EXCLUDED.program_name,
      effective_since = EXCLUDED.effective_since;
"""

def load_programs():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(SQL, ROWS)
        print(f"✅  Loaded/updated {len(ROWS)} program offerings.")
    finally:
        conn.close()
