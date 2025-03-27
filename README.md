# Flight fetcher :airplane:
This project has been built to automatically fetch data from the [flightaware](https://www.flightaware.com/live/) webpage and to automatically store them using a relational database (like PostgreSQL). 
For it, I have used the `requests` package and have splitted the world's map into a grid of several squares.
This division is important because, for some reason, the GET request will not give you all planes on the air if you query for the whole worls at once.
The world grid looks something like this:

![image](https://github.com/user-attachments/assets/759cdedc-9b1e-4f62-88fb-bae7a942c5c0)

The model then triggers the GET request for each square and gets all the metadata of all the aircrafts flying within that space.
I had particular fun while designing this project as it is usually very difficult to fetch information from these webs using conventional scraping like Selenium or BeautifulSoup, but still managed to get it through basic HTTP methods. 

## Project features

- **Flight extraction**: Fetches metadata and stock data (OHLCV) for different stocks. An Alphavantage API key is needed. Can be requested following this [link](https://www.alphavantage.co/support/#support).
- **Data storage**: Stores the data in a PostgreSQL database.
- **Email notification**: Sends a success notification after the process is complete. E-mail credentials are needed in order to enable this feature.
- **Logging**: Comprehensive logging of the process. Can be useful both for reporting and debugging.

## Requirements

Before running this project, ensure you have the following dependencies installed:

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

## Installation

### Clone the repository

```bash
git clone git@github.com:schrutebeet/stock_market.git
cd stock_market
```

## Additional resources
The project also contains the following files:

- `Dockefile`: A Docker file which can be used to build an image of this project and deploy it anywhere. I personally use this option to deploy the project on a Raspberry Pi 3B.
- `stocks_cronjob.sh`: If using images is an expensive option for deploying, you can also add this file as a Cronjob task to be executed in your computer.
