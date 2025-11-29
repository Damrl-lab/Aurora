import psycopg2
import pandas as pd
from datetime import datetime

def store_course_job_similarity(csv_path, method=None):
    df = pd.read_csv(csv_path)

    conn = psycopg2.connect(
        dbname="course_job_fit",
        user="postgres",
        password="yourpassword",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO course_job (course_id, job_id, similarity_score, ranking, alignment_date)
            VALUES (
                (SELECT course_id FROM Courses WHERE course_title = %s LIMIT 1),
                (SELECT job_id FROM Job_Postings WHERE job_title = %s LIMIT 1),
                %s, NULL, %s
            )
            ON CONFLICT (course_id, job_id) DO UPDATE
            SET similarity_score = EXCLUDED.similarity_score,
                alignment_date = EXCLUDED.alignment_date;
        """, (
            row['Course Name'],
            row['Job Title'],
            row['Similarity'],
            datetime.now()
        ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Stored {len(df)} similarity records to 'course_job' table.")
