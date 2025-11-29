#!/usr/bin/env bash
set -eo pipefail

echo "🏁 waiting for Postgres…"
for i in $(seq 1 30); do
  if python - <<'PY'
import os, psycopg2, sys
try:
    psycopg2.connect(os.environ["PG_DSN"]).close()
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
  then
    echo "✅ Postgres is up"
    break
  else
    echo "ℹ️  Postgres not up yet (attempt $i)…"
  fi
  sleep 1
done

# echo "🗃 dumping courses table → Prolog facts…"
# python dump_facts.py    # writes courses_facts.pl

echo "🚦 loading Prolog KB + starting validator…"
exec uvicorn validator:app --host 0.0.0.0 --port 8000
