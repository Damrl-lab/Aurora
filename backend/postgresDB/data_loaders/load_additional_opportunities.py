import os, sys

# import of db_config.py from the parent directory
script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)
from db_config import get_connection

# ── 1) Fields in Additional_Opportunities:
#    (opportunity_name, opportunity_type, opportunity_description,
#     contact_info, location, prerequisites, opportunity_url, membership_requirements)
# ────────────────────────────────────────────────────────────────────

OPPORTUNITIES = [
    (
        "Data Management Research Laboratory (DaMRL)",
        "Research Lab",
        "Lab researching flash-based storage, big-data processing, "
        "cloud/HPC architectures, and performance/resource management.",
        "jbhimani@fiu.edu",      # DaMRL director 
        "CASE 238B",
        None,
        "https://damrl.cs.fiu.edu/",
        "Open via RA/REU appointments"
    ),
    (
        "Bioinformatics Research Group (BioRG)",
        "Research Group",
        "Interdisciplinary research in genomics, metagenomics, "
        "pattern discovery, transcriptome analysis, medical imaging, and data mining.",
        "gnarasim@cis.fiu.edu",   # BioRG director 
        "CASE 254B",
        None,
        "https://biorg.cs.fiu.edu/",
        "Contact PI for membership"
    ),
    (
        "SOLID Lab",
        "Research Lab",
        "Machine-learning and optimization for cyber-physical systems resilience, "
        "security, and infrastructure.",
        "bc@cis.fiu.edu",         # SOLID Lab homepage 
        "CASE 238",
        None,
        "https://www.solidlab.fiu.edu/",
        "Open by application"
    ),
    (
            "CAESCIR",
            "Research Center",
        "DHS-funded center for research & education on critical-infrastructure resilience.",
        "iyengar@cis.fiu.edu",    # Prof. S. S. Iyengar 
        "ECS 351",
        None,
        "https://caescir.cis.fiu.edu/",
        "Open to student & postdoc applicants"
    ),
    (
        "Southeast Florida Coastal Environmental Data & Modeling Center",
        "Research Center",
        "Collaborative AI/ML research on sea-level rise, flooding, and HAB detection.",
        "jliu8@cis.fiu.edu",      # Prof. Jason Liu 
        "FIU Institute of Environment",
        None,
        "https://www.cis.fiu.edu/new-south-florida-coastal-environmental-data-and-modeling-center/",
        "Open to researchers"
    ),
    (
        "Center for Diversity in Engineering & Computing",
        "Research Center",
        "Promotes inclusive research & workforce training for underrepresented groups.",
        "mmilani@cis.fiu.edu",    # Prof. Masoud Milani 
        "ECS 388",
        None,
        "https://cec.fiu.edu/academics/student-resources/cd-ssec",
        "Open to all FIU students"
    ),
    (
        "Graduate Applications Office",
        "Academic Support Service",
        "Guidance for CIS graduate program applicants.",
        "rarocha@fiu.edu",               # Graduate Applications :contentReference[oaicite:7]{index=7}
        "CASE 350",
        None,
        "https://admissions.fiu.edu/how-to-apply/graduate-applicant/",
        "Prospective graduate students"
    ),
    (
        "Peer Tutoring (STARS & ASI)",
        "Tutoring & Mentoring",
        "Free peer-to-peer tutoring for CIS courses.",
        "tutoring@cis.fiu.edu",          # Peer tutoring :contentReference[oaicite:8]{index=8}
        None,
        None,
        "https://www.cis.fiu.edu/students/tutoring/",
        "Enrolled CIS students"
    ),
    (
        "UKG Academy for Computer Science and Education - Programming Team",
        "Student Organization",
        "Competitive programming training and contest participation.",
        None,
        None,
        None,
        "https://academy.cis.fiu.edu/programming-team/",
        "Open to CIS students"
    ),
    (
        "ACM Student Chapter",
        "Student Organization",
        "Local chapter of the Association for Computing Machinery.",
        None,
        None,
        None,
        "https://acm.cs.fiu.edu/",
        "Membership via ACM"
    ),
    (
        "Women in CS (WiCS)",
        "Student Organization",
        "Promotes gender equity in computing through events and community.",
        None,
        None,
        None,
        "https://wics.cs.fiu.edu/",
        "Open to FIU students"
    ),
    (
        "Women in CyberSecurity (WiCyS)",
        "Student Organization",
        "Supports women in cybersecurity with networking and hands-on workshops.",
        None,
        None,
        None,
        "https://wicys.cs.fiu.edu/",
        "Open to FIU students"
    ),
    (
        "Hackathons",
        "Extracurricular Activity",
        "Multi-day coding competitions for project prototyping.",
        None,
        None,
        None,
        "https://shellhacks.net/",  # :contentReference[oaicite:9]{index=9}
        "Open teams of 3–5"
    ),
    (
        "Workshops & Short Courses",
        "Professional Development",
        "Hands-on industry-led sessions on programming, web/dev, and robotics.",
        None,
        None,
        None,
        "https://cec.fiu.edu/academics/student-resources/career-services/professional-development-workshops-events",   # :contentReference[oaicite:12]{index=12}
        "Open to FIU community"
    ),
    (
        "KFSCIS Seminar Series",
        "Lecture Series",
        "Weekly guest-speaker seminars on cutting-edge computing topics.",
        "seminars@cis.fiu.edu",           # :contentReference[oaicite:13]{index=13}
        None,
        None,
        "https://www.cis.fiu.edu/lecture_series/kfscis-seminar-series/",
        "Open to FIU community"
    ),
    (
        "Tech Talent Academy",
        "Industry Partnership",
        "Industry-oriented micro-credential training for career readiness.",
        None,
        None,
        None,
        "https://techtalent.fiu.edu/",  # :contentReference[oaicite:15]{index=15}
        "Open to CIS students"
    ),
    (
        "Break Through Tech Miami (BTT FIU)",
        "Student Organization",
        "Hands-on programs—3-week paid Sprinternships™, 7-week technical workshops, and semester-long Data Corps—designed to break barriers and equip FIU students (especially women and underrepresented groups) with real-world tech skills and industry experience.",
        "brkthrtech@fiu.edu",
        "CASE 266, 11200 SW 8th Street, Miami, FL 33199",
        None,
        "https://miami.breakthroughtech.org/",
        "Open to all FIU students; application required"
    ),
    (
        "FIU Discovery Lab",
        "Undergraduate Research Lab",
        "Undergraduate research lab providing FIU students with hands-on exposure to robotics, machine learning, digital forensics, quantum computing, sensor systems and advanced visualization.",
        "discoverylab@cis.fiu.edu",
        "ECS 232",
        None,
        "https://discoverylab.cis.fiu.edu/",
        "Open to undergraduate researchers"
    ),
    (
        "Career & Talent Development",
        "Career Services Center",
        "FIU’s central student & alumni career resource offering resume critiques, professional-development workshops, employer networking events and internship/job-search assistance.",
        None,
        "EC 2852 (next to Panther Pit)",
        None,
        "https://career.fiu.edu/",
        "Open to FIU students and alumni"
    ),

]

# ── 2) Transform into DB rows ──────────────────────────────────────
rows = [
    (
        name, typ, desc,
        contact, location, prereqs,
        url, membership
    )
    for (name, typ, desc, contact, location, prereqs, url, membership)
    in OPPORTUNITIES
]

# ── 3) Upsert into Additional_Opportunities ───────────────────────
SQL = """
INSERT INTO Additional_Opportunities
  (opportunity_name, opportunity_type, opportunity_description,
   contact_info, location, prerequisites,
   opportunity_url, membership_requirements)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (opportunity_name) DO UPDATE
  SET opportunity_type          = EXCLUDED.opportunity_type,
      opportunity_description   = EXCLUDED.opportunity_description,
      contact_info              = EXCLUDED.contact_info,
      location                  = EXCLUDED.location,
      prerequisites             = EXCLUDED.prerequisites,
      opportunity_url           = EXCLUDED.opportunity_url,
      membership_requirements   = EXCLUDED.membership_requirements;
"""

def load_opportunities():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(SQL, rows)
        print(f"✅  Upserted {len(rows)} additional opportunities.")
    finally:
        conn.close()
