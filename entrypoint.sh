#!/bin/sh

poetry run alembic upgrade head
 
# poetry run fastapi run madr_novels/app.py --host 0.0.0.0
poetry run uvicorn --host 0.0.0.0 --port 8000 madr_novels.app:app