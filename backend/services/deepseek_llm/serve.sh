#!/usr/bin/env bash
# lightweight wrapper
exec uvicorn server:app --host 0.0.0.0 --port 8001 --workers 1
