# postgresDB/init_schema.py
from db_config import get_connection
from dotenv    import load_dotenv
import os, sys

load_dotenv()


def execute_schema_sql() -> None:
    """
    Creates / upgrades the Postgres schema:

      • executes schema.sql (tables, FK, etc.)
      • installs pgvector
      • ensures courses.embedding vector(384) column exists
    """
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

    # ---------- read file -------------------------------------------------
    with open(schema_path, encoding="utf-8") as f:
        schema_sql = f.read()

    # ---------- connect ---------------------------------------------------
    conn = None
    try:
        conn = get_connection()          # ← your helper returns psycopg connect()
        conn.autocommit = True           # one batch → no need for explicit commit

        with conn.cursor() as cur:
            # main DDL
            cur.execute(schema_sql)

            # pgvector >= 0.6 – the extension is now called *vector*
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

            # embedding columns (idempotent)
            cur.execute("""
              ALTER TABLE courses
              ADD COLUMN IF NOT EXISTS embedding vector(384)
            """)
            
            # cur.execute("""
            #   ALTER TABLE IF EXISTS job_postings
            #   ADD    COLUMN IF NOT EXISTS embedding vector(384);   # ← new line
            # """)

        print("✅  Schema initialized / migrated.")
    except Exception as exc:
        print("❌  Error initializing schema:", exc, file=sys.stderr)
        sys.exit(1)                      # make the Compose job fail visibly
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    execute_schema_sql()
