from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from models import Data, get_db

app = FastAPI()

@app.get("/data")
def get_data(
    start: datetime,
    end: datetime,
    variables: List[str] = Query(default=["wind_speed", "power", "ambient_temperature"]),
    db: Session = Depends(get_db)
):
    allowed_vars = {"wind_speed", "power", "ambient_temperature"}
    selected_vars = [var for var in variables if var in allowed_vars]

    columns = [getattr(Data, "timestamp")] + [getattr(Data, var) for var in selected_vars]

    query = db.query(*columns).filter(Data.timestamp >= start, Data.timestamp <= end)

    results = [
        dict(zip(["timestamp"] + selected_vars, row))
        for row in query.all()
    ]
    
    return results