# SimpleETL

This is a simple ETL (Extract, Transform, Load) project that uses FastAPI and PostgreSQL. The project is designed to extract data from a source database, transform it, and load it into a target database. The project is containerized using Docker and Docker Compose.

Data is created from 2025-01-01 to 2025-01-10.

In order to run tests, first create a `.env` file in the root directory of the project. This file should contain the following environment variables:

* `SOURCE_DB_URL`: The URL for the source database (PostgreSQL).
* `TARGET_DB_URL`: The URL for the target database (PostgreSQL).
* `POSTGRES_USER`: The username for the PostgreSQL database.
* `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
* `POSTGRES_DB`: The name of the PostgreSQL database (for now, we are using the same database for both source and target).
* `API_URL`: The URL for the API endpoint inside docker.

Example .env file:
```env
SOURCE_DB_URL=postgresql+psycopg2://postgres:abc123@source_db:5432/test
TARGET_DB_URL=postgresql+psycopg2://postgres:abc123@target_db:5432/test
POSTGRES_USER=postgres
POSTGRES_PASSWORD=abc123
POSTGRES_DB=test
API_URL=http://api:8000
```


## Running the Project

```bash
# Build and run the Docker containers
docker-compose up --build

# Insert data into the source database
docker exec fastapi_app python populate_db.py
```

After running the above commands, the FastAPI application will be available at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

Dagster webserver will be available at `http://localhost:3000`. There, you can observe the ETL process and monitor the status of the jobs.

To run the ETL process bypassing the Dagster webserver, you can use the following command:
```bash
# Run the ETL process (for example, for the date 2025-01-01)
docker exec etl-container python etl/etl.py 2025-01-01
```