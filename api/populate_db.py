from datetime import datetime, timedelta
import random
from models import Data, init_db, get_db

def generate_random_data(session, n_minutes, base_time):
    for i in range(n_minutes):
        data = Data(
            timestamp = base_time + timedelta(minutes=i),
            wind_speed = random.uniform(0, 100),
            power = random.uniform(0, 100),
            ambient_temperature = random.uniform(0, 40),
        )
        session.add(data)
    session.commit()

if __name__ == "__main__":
    base_time = datetime(2025, 1, 1)
    n_minutes = 60 * 24 * 10  # 10 days of data

    init_db()
    
    db = next(get_db())  # Get a session from the generator
    generate_random_data(db, n_minutes, base_time)

    print(f"Inserted {n_minutes} records into the database starting from {base_time}.")