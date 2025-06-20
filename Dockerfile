FROM python:3.13-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install poetry --default-timeout=100 future

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev

EXPOSE 8000
# CMD poetry run fastapi run madr_novels/app.py --host 0.0.0.0
CMD poetry run uvicorn --host 0.0.0.0 madr_novels.app:app