# Flight fetcher :airplane:
This project has been built to automatically fetch data from the [flightaware](https://www.flightaware.com/live/) webpage and to automatically store them using a relational database (like PostgreSQL). 
For it, I have used the `requests` package and have splitted the world's map into a grid of several squares.
This division is important because, for some reason, the GET request will not give you all planes on the air if you query for the whole worls at once.
The world grid looks something like this:

![image](https://github.com/user-attachments/assets/759cdedc-9b1e-4f62-88fb-bae7a942c5c0)

The model then triggers the GET request for each square and gets all the metadata of all the aircrafts flying within that space.
I had particular fun while designing this project as it is usually very difficult to fetch information from these webs using conventional scraping like Selenium or BeautifulSoup, but still managed to get it through basic HTTP methods. 

## Project features

- **Flight extraction**: Fetches several information features for each flight in the air. There are approximately 12,000 flights traveling from one place to another at any point in time. Data contains key information like:
    - `Coordinates` both for latitude and longitude.
    - Flight `prefix`
    - Flight `identification` number.
    - Radiant `direction`. From 0º to 360º.
    - `Flight type` indicating whether the aircraft is an _airline_, an _cargo_, _medical evacuation_ aircraft, etc.
    - `Ground speed`
    - ...and many more!
- **Data storage**: Store the dataframes locally using parquet files for disk optimization.

## Requirements

Before running this project, ensure you have the following dependencies installed:

- Python 3.x
- poetry 1.8.0
- Required Python packages (to be installed using `poetry install`)

## Installation

### Clone the repository

```bash
git clone git@github.com:schrutebeet/flights.git
cd flights
```


## Planning ahead
The next steps for this project include:

- **Logging**: Comprehensive logging of the process. To be used both for reporting and debugging.
- **Email notification**: To be used at the end of each run, or at the end of the day.
- **Data storage**: So far, only parquet files are used. Data could be stored in a database for better fault tolerance.
