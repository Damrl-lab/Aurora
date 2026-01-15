"""
Embedding Service (Future Extension)

Provides vector similarity search using sentence-transformers embeddings
stored in PostgreSQL with pgvector. Currently disconnected from the main
pipeline - Aurora uses SQL + Prolog for retrieval instead.
"""
import os, psycopg, numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

from pgvector.psycopg import register_vector, Vector

PG_DSN = os.getenv("PG_DSN")
model  = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

app = FastAPI(title="Vector Lookup / Similarity Service")


def get_conn() -> psycopg.Connection:
    """Create a PostgreSQL connection with pgvector support."""
    conn = psycopg.connect(PG_DSN)
    register_vector(conn)
    return conn


class KNNQuery(BaseModel):
    text          : str
    candidate_ids : list[str] = Field(default_factory=list)
    top_k         : int       = Field(5, ge=1, le=50)


def as_vec(x: np.ndarray) -> Vector:
    # pgvector stores 32-bit floats 
    return Vector(x.astype("float32").tolist())


@app.post("/query_knn")
def query_knn(q: KNNQuery):
    """Find k-nearest courses by embedding similarity to query text."""
    emb = as_vec(model.encode(q.text, normalize_embeddings=True))

    where_clause = "TRUE"
    params = {"v": emb, "k": q.top_k} 

    if q.candidate_ids:
        where_clause = "course_id = ANY(%(cand)s)"
        params["cand"] = q.candidate_ids

    sql = f"""
      SELECT course_id
        FROM courses
       WHERE {where_clause}
    ORDER BY embedding <=> %(v)s
       LIMIT %(k)s
    """

    with get_conn() as conn, conn.cursor() as cur:
        ids = [row[0] for row in cur.execute(sql, params).fetchall()]

    return {"ids": ids}
