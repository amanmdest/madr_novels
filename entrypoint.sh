#!/bin/sh

poetry run alembic upgrade head
 
poetry run fastapi run madr_novels/app.py --host 0.0.0.0