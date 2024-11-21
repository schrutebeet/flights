from flights_fetcher import FlightsFetcher
from data_manager import DataManager

flights = FlightsFetcher("https://www.flightaware.com/live/")

last_hour = None

while True:
    list_of_flights = flights.run_all()
    print("All flights fetched.")
    df = DataManager.preprocess_data(list_of_flights)
    print("Flights converted to dataframe.")
    DataManager.save_to_temp(df)
    print("Flights dataframe saved in tmp folder.")
    last_hour = DataManager.process_hourly_data()
    print(f"All files from {last_hour}h have been concatenated and stored.")
