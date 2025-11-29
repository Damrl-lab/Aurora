# data_loaders/load_all.py
import os
from db_config import get_connection

from load_majors     import load_majors
from load_program_offerings     import load_programs
from load_courses    import load_courses
from load_program_course    import load_program_course
from load_categories    import load_categories
from load_job_postings      import load_jobs
from load_course_category_rank  import load_course_rank
from load_skills     import load_skills
from load_course_skills import load_course_skill
from load_job_skills import load_job_skill
from load_faculty   import load_faculty
from load_additional_opportunities  import load_opportunities
from load_program_resource  import load_program_resource
from load_career_advisor    import load_career_advisor
from load_career_advisor_opportunity    import load_career_advisor_opportunity
from load_users_students    import load_user_student
from load_user_course   import load_user_course
from load_user_program  import load_user_program
from load_user_resource import load_user_resource
from load_academic_advisor  import load_academic_advisor
from load_academic_advisor_student import load_academic_advisor_student


BASE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
SCHEMA_FILE = os.path.join(BASE, "postgresDB", "schema.sql")

def main():
    conn = get_connection()         
    # with open(SCHEMA_FILE) as f:
    #     ddl = f.read()
    # with conn.cursor() as cur:
    #     cur.execute(ddl)
    # conn.commit()
    # print("✅ Schema created")

    # load tables in the correct order
    load_majors()
    load_programs()
    load_courses()
    load_program_course()
    load_categories()
    load_jobs()
    load_course_rank()
    load_skills()
    load_course_skill()
    load_job_skill()
    load_faculty()
    load_opportunities()
    load_program_resource()
    load_career_advisor()
    load_career_advisor_opportunity()
    load_user_student()
    load_user_course() 
    load_user_program() 
    load_user_resource()
    load_academic_advisor()
    load_academic_advisor_student()  
    

    print("🎉 All data loaded!")

if __name__ == "__main__":
    main()
