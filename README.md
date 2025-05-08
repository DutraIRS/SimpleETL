# SimpleETL

Example .env file:
```env
SOURCE_DB_URL=postgresql+psycopg2://postgres:abc123@source_db:5432/test
TARGET_DB_URL=postgresql+psycopg2://postgres:abc123@target_db:5432/test
POSTGRES_USER=postgres
POSTGRES_PASSWORD=abc123
POSTGRES_DB=test
API_URL=http://api:8000
```

```bash
# Build and run the Docker containers
docker-compose up --build

# Insert data into the source database
docker exec fastapi_app python populate_db.py

# Run the ETL process
docker exec etl-container python etl/etl.py 2025-01-01
```