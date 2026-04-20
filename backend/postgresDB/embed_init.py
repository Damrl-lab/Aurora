"""
Fill pgvector column for the Courses table only.
Idempotent – only rows where `embedding IS NULL`.
"""

from __future__ import annotations
import os, psycopg, numpy as np
from sentence_transformers import SentenceTransformer
from pgvector.psycopg import Vector, register_vector

# ───────────── DSN
user  = os.getenv("POSTGRES_USER")
pw    = os.getenv("POSTGRES_PASSWORD")
host  = os.getenv("POSTGRES_HOST", "vector_db")
port  = os.getenv("POSTGRES_PORT", "5432")
db    = os.getenv("POSTGRES_DB")
PG_DSN = os.getenv("PG_DSN") or f"postgresql://{user}:{pw}@{host}:{port}/{db}"

# ───────────── model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cpu"
)

def encode(txt: str) -> Vector:              # return the right type
    vec = model.encode(txt or "",
                       normalize_embeddings=True).astype("float32")
    return Vector(vec.tolist())

with psycopg.connect(PG_DSN, autocommit=True) as conn:
    register_vector(conn)
    cur = conn.cursor()
    cur.execute("""
        SELECT course_id,
               course_title || ' ' || COALESCE(course_description,'')
        FROM courses
        WHERE embedding IS NULL
        LIMIT 100000
    """)
    rows = cur.fetchall()
    for cid, text in rows:
        cur.execute(
            "UPDATE courses SET embedding = %s WHERE course_id = %s",
            (encode(text), cid)
        )

print(f"✅  {len(rows)} course embeddings written")
