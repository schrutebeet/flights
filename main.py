from flights_fetcher import FlightsFetcher
from data_manager import DataManager

flights = FlightsFetcher("https://www.flightaware.com/live/")

last_hour = None

while True:
    list_of_flights = flights.run_all()
    df = DataManager.preprocess_data(list_of_flights)
    DataManager.save_to_temp(df)
    last_hour = DataManager.process_hourly_data()
