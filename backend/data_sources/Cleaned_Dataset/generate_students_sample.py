#!/usr/bin/env python3
import pandas as pd
import random
import string
import hashlib
from datetime import date, timedelta
from faker import Faker

fake = Faker()

NUM_STUDENTS = 100
OUTPUT_PATH   = "Cleaned Dataset\sample_students_and_enrollments.xlsx"

# must match your Program_Offerings.program_code values
PROGRAM_CODES = [
    "CS-BA", "CS-BS", "CS-BS-SDD", "CS-MINOR",
    "DS-BS", "MS-CS", "MS-DS", "PHD-CS",
    "IT-BA", "IT-BS", "IT-BS-SW", "PM-CERT"
]

CAREER_INTERESTS = [
    "Data Analytics", "Machine Learning", "Network Security",
    "Software Development", "Cloud Computing", "Product Management",
    None
]

def gen_user_id() -> str:
    return ''.join(random.choices(string.digits, k=7))

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

students = []
enrollments = []

for _ in range(NUM_STUDENTS):
    uid        = gen_user_id()
    fn         = fake.first_name()
    ln         = fake.last_name()
    email      = f"{fn.lower()}.{ln.lower()}@fiu.edu"
    status     = random.choice(["active","completed"])
    career     = random.choice(CAREER_INTERESTS)
    raw_pw     = fake.password(length=12,
                               special_chars=True,
                               digits=True,
                               upper_case=True,
                               lower_case=True)
    pw_hash    = hash_password(raw_pw)

    # pick a program and enrollment dates
    prog       = random.choice(PROGRAM_CODES)
    start_off  = random.randint(0, 4*365)
    start_dt   = date.today() - timedelta(days=start_off)
    if status == "completed":
        end_dt = start_dt + timedelta(days=random.randint(3*365,4*365))
    else:
        end_dt = None

    students.append({
        "user_id":         uid,
        "first_name":      fn,
        "last_name":       ln,
        "email":           email,
        "status":          status,
        "career_interest": career,
        "password_hash":   pw_hash
    })

    enrollments.append({
        "user_id":      uid,
        "program_id":   prog,
        "start_date":   start_dt,
        "end_date":     end_dt,
        "status":       status
    })

with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
    pd.DataFrame(students).to_excel(writer, sheet_name="Students", index=False)
    pd.DataFrame(enrollments).to_excel(writer, sheet_name="User_Program", index=False)

print(f"✅  Wrote {NUM_STUDENTS} students + enrollments to '{OUTPUT_PATH}'")
