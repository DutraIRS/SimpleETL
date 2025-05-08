
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'etl')))

from models import init_db, get_db
from etl import register_signal, run_etl

from dagster import (
    asset,
    DailyPartitionsDefinition,
    Definitions,
    resource,
    define_asset_job,
    build_schedule_from_partitioned_job
)

from dotenv import load_dotenv
load_dotenv('.env')

# ---------- Recursos ----------
@resource
def source_db():
    return next(get_db())

@resource
def target_db():
    return next(get_db())

# ---------- ETL ----------
API_URL = os.getenv("API_URL")

# ---------- Dagster Asset ----------
daily_partition = DailyPartitionsDefinition(start_date="2025-01-01")

@asset(partitions_def=daily_partition, required_resource_keys={"source_db", "target_db"})
def daily_update(context):
    source_db = context.resources.source_db
    target_db = context.resources.target_db
    date_str = context.partition_key
    context.log.info(f"Iniciando ETL para {date_str}")

    init_db()
    signal_id = register_signal(target_db, date_str)
    run_etl(source_db, date_str, signal_id)

    context.log.info("ETL finalizado.")

# ---------- Job e Schedule ----------
daily_update_job = define_asset_job(name="daily_update_job", selection=["daily_update"])

daily_update_schedule = build_schedule_from_partitioned_job(
    job=daily_update_job
)

# ---------- Definitions ----------
defs = Definitions(
    assets=[daily_update],
    resources={"source_db": source_db, "target_db": target_db},
    jobs=[daily_update_job],
    schedules=[daily_update_schedule],
)
