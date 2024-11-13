from flights_fetcher import FlightsFetcher


flights = FlightsFetcher("https://www.flightaware.com/live/")
flights.run_all()