import sys
import httpx
import pandas as pd
from datetime import datetime, timedelta
from models import init_db, get_db, Trigger, Signal

import os
from dotenv import load_dotenv

load_dotenv('.env')

API_URL = os.getenv("API_URL")

def register_signal(db, reference_date, origin='mock-origin'):
    now_timestamp = datetime.now()
    
    trigger = Trigger(timestamp=now_timestamp, origin=origin, date=reference_date)
    
    db.add(trigger)
    db.commit()
    db.refresh(trigger)
    
    return trigger.id

def process_data(data):
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    
    data_dict = {
        'max': df.resample('10min').max().reset_index(),
        'min': df.resample('10min').min().reset_index(),
        'mean': df.resample('10min').mean().reset_index(),
        'std': df.resample('10min').std().reset_index()
    }
    
    return data_dict

def create_signals(data_dict, signal_id):
    signals = []
    for stat, df_stat in data_dict.items():
        for col in df_stat.drop(columns=['timestamp']).columns:
            for _, row in df_stat.iterrows():
                signal = Signal(
                    name=col,                       # eg "wind_speed"
                    data=stat,                      # eg "max"
                    timestamp=row['timestamp'],     # eg "2025-01-01 00:00:00"
                    signal_id=signal_id,            # eg 341
                    value=row[col]                  # eg 42.42
                )
                signals.append(signal)
    
    return signals

def run_etl(db, date, signal_id):
    start = datetime.strptime(date, "%Y-%m-%d")
    end = start + timedelta(days=1) - timedelta(seconds=1)
    
    params = {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "variables": ["wind_speed", "power"]
    }
    
    response = httpx.get(API_URL + "/data", params=params)
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return

    data = response.json()
    
    data_dict = process_data(data)
    signals = create_signals(data_dict, signal_id)
    
    for signal in signals:
        db.add(signal)
    
    db.commit()
    
    print(f"ETL process completed for {date}. Data saved to database.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python etl.py YYYY-MM-DD")
        sys.exit(1)
    
    date = sys.argv[1]
    
    init_db()
    
    db = next(get_db())
    signal_id = register_signal(db, date)
    
    run_etl(db, date, signal_id)

if __name__ == '__main__':
    main()