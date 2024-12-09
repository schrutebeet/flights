import time
from datetime import datetime

from flights_fetcher import FlightsFetcher
from data_manager import DataManager

flights = FlightsFetcher("https://www.flightaware.com/live/")

last_hour = None

while True:
    s = datetime.now()
    list_of_flights = flights.run_all()
    print("All flights fetched.")
    df = DataManager.preprocess_data(list_of_flights)
    print(f"{len(df)} flights converted to dataframe.")
    DataManager.save_to_temp(df)
    last_hour = DataManager.process_hourly_data(last_hour=last_hour)
    e = datetime.now()
    time_difference = (e - s).total_seconds()
    if time_difference < 60:
        sleep_time = 60 - time_difference
        time.sleep(sleep_time)
        print(f"Triggered time sleep for {sleep_time:.2f} seconds.")
    print("\n")
