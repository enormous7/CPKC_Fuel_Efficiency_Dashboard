import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_fuel_data(num_records=2000):
    """
    Generates simulated CPKC train operational and fuel consumption data.
    Factors influencing fuel consumption include speed, train weight, distance,
    and simulated weather conditions.
    """
    print(f"Generating {num_records} records of simulated CPKC train fuel data...")

    start_date = datetime(2023, 1, 1)
    train_ids = [f"TRN{i:04d}" for i in range(1, 101)] # 100 unique trains
    routes = ["Vancouver-Calgary", "Winnipeg-Toronto", "Chicago-Kansas City", "Montreal-Detroit", "Edmonton-Regina"]

    data = []
    for _ in range(num_records):
        timestamp = start_date + timedelta(hours=random.randint(0, 365 * 24))
        train_id = random.choice(train_ids)
        route = random.choice(routes)
        distance_km = random.randint(300, 2500) # Distance for the segment

        avg_speed_kmh = random.uniform(40, 90) # Average speed

        # Simulate train weight (tons)
        train_weight_tons = random.randint(3000, 15000) 

        # Simulate weather conditions (0: Clear, 1: Rain/Snow, 2: Heavy Wind)
        weather_condition = random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1], k=1)[0]

        # Base fuel consumption (liters/km) - higher for heavier trains and higher speed
        base_fuel_rate = 0.05 + (train_weight_tons / 100000) + (avg_speed_kmh / 1000)

        # Add impact of weather (increases fuel consumption)
        if weather_condition == 1: # Rain/Snow
            base_fuel_rate *= random.uniform(1.05, 1.15)
        elif weather_condition == 2: # Heavy Wind
            base_fuel_rate *= random.uniform(1.15, 1.30)

        # Add randomness
        fuel_consumption_liters = (base_fuel_rate * distance_km) * random.uniform(0.9, 1.1)

        data.append({
            "Timestamp": timestamp,
            "Train_ID": train_id,
            "Route": route,
            "Distance_km": distance_km,
            "Avg_Speed_kmh": avg_speed_kmh,
            "Train_Weight_tons": train_weight_tons,
            "Weather_Condition": weather_condition, # 0=Clear, 1=Rain/Snow, 2=Heavy Wind
            "Fuel_Consumed_liters": fuel_consumption_liters
        })

    df = pd.DataFrame(data)
    print("Data generation complete.")
    return df

if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)

    df = generate_fuel_data(5000) # Generate 5000 records for better model training

    output_file = os.path.join(output_dir, 'cpkc_train_fuel_data.csv')
    df.to_csv(output_file, index=False)
    print(f"Simulated data saved to: {output_file}")