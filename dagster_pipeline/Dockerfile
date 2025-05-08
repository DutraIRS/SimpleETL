FROM python:3.13-slim

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

RUN pip install -r dagster_pipeline/requirements.txt

EXPOSE 3000

CMD ["dagster", "dev", "-f", "dagster_pipeline/dagster_pipeline/definitions.py", "--working-directory", "/app", "--host", "0.0.0.0"]
