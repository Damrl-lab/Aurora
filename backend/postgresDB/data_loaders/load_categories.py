"""
load_categories.py  –  populate the Category lookup table
---------------------------------------------------------
Table definition (per schema):
    category_id   VARCHAR(16) PRIMARY KEY
    name          TEXT UNIQUE NOT NULL
"""

import os, sys

# import of db_config.py from the parent directory
script_dir = os.path.dirname(__file__)              
parent_dir = os.path.dirname(script_dir)            
sys.path.append(parent_dir)
from db_config import get_connection

ROWS = [
    ("CS",  "Computer Science"),
    ("DS",  "Data Science"),
    ("IT",  "Information Technology"),
    ("SWE", "Software Engineering"),
    ("PM",  "Product Management"),
]

SQL = """
INSERT INTO Category (category_id, name)
VALUES (%s, %s)
ON CONFLICT (category_id) DO UPDATE
   SET name = EXCLUDED.name;
"""

def load_categories():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(SQL, ROWS)
        print(f"✅  Loaded/updated {len(ROWS)} categories.")
    finally:
        conn.close()

