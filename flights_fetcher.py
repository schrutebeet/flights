import re
import time
import json
import random
from pathlib import Path
from typing import List, Dict, Any, Union, Tuple, Iterator

import requests
from playwright.sync_api import sync_playwright

ROOT_PATH = Path(__file__).parent

class FlightsFetcher:

    MIN_LONGITUDE = -180
    MAX_LONGITUDE = 180
    MIN_LATITUDE = -90
    MAX_LATITUDE = 90

    def __init__(self, webpage_url: str):
        self.webpage_url = webpage_url

    def run_all(self) -> None:
        url_aircraft_list = self.get_webpage_url_calls()
        airplane_url = next((item for item in url_aircraft_list if "vicinity_aircraft" in item), None)
        airplane_url_template = self.replace_coordinates_with_placeholders(airplane_url)
        self.create_long_lat_sections(sections=50)
        sum_planes = 0
        for minLon, maxLon, minLat, maxLat in self.iterate_coordinates():
            coordinates_dict = {"minLon": minLon, "maxLon": maxLon, "minLat": minLat, "maxLat": maxLat}
            airplane_url = airplane_url_template.format(**coordinates_dict)
            result = self.get_json_from_api_call(airplane_url)
            time.sleep(random.randint(1, 3))
            result = result["features"]
            sum_planes = sum_planes + len(result)
            print(sum_planes)


    def get_webpage_url_calls(self, filter_by: str = None) -> List[str]:
        with sync_playwright() as p:
            # Launch the browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            # List to store captured URLs
            urls = []
            # Set up a network request listener
            page.on("request", lambda request: urls.append(request.url))
            # Open the page
            page.goto(self.webpage_url)
            # Close the browser
            browser.close()
        if filter_by:
            urls = [url for url in urls if f"{filter_by}" in url]
        return urls

    def get_aircraft_token(self, url_list: List[str]) -> Union[str, None]:
        for url in url_list:
            if "vicinity_aircraft" in url:
                pattern = r'token=([a-f0-9]{40})'
                match = re.search(pattern, url)
                if match:
                    token = match.group(1)
                    return token

    def get_json_from_api_call(self, url: str) -> Dict[str, Any]:
        with open(ROOT_PATH / "support/files/user_agents.json", 'r') as file:
            user_agents_list = json.load(file)
        user_agent = random.choice(user_agents_list)
        header = {'user-agent': user_agent}
        s = requests.Session()
        s.headers.update(header)
        json_data = s.get(url).json()
        return json_data

    def create_long_lat_sections(self, sections: int, file_path: Union[Path, str] = None) -> None:
        """Create a .txt file with different sections covering the whole coordinates space.
        The more {sections}, the more the space will be divided.

        Args:
            sections (int): number of sections in which the space needs to be divided.
        """
        longitude_step = (self.MAX_LONGITUDE - self.MIN_LONGITUDE) / sections
        latitude_step = (self.MAX_LATITUDE - self.MIN_LATITUDE) / sections
        # Open a file to write the coordinates
        if file_path is None:
            file_path = ROOT_PATH / "support/files"
        with open(f"{file_path}/map_sections.txt", "w") as file:
            for i in range(sections):
                # Calculate the longitude range for each section
                lon_min = self.MIN_LONGITUDE + i * longitude_step
                lon_max = lon_min + longitude_step
                # For simplicity, we’re keeping the latitude range constant
                lat_min = self.MIN_LATITUDE
                lat_max = self.MAX_LATITUDE
                # Write to file in the format: MIN_LONGITUDE, MIN_LATITUDE, MAX_LONGITUDE, MAX_LATITUDE
                file.write(f"{lon_min},{lat_min},{lon_max},{lat_max}\n")

    @staticmethod
    def iterate_coordinates(file_path: Union[Path, str] = None) -> Iterator[Tuple[Tuple[float, float], Tuple[float, float]]]:
        if file_path is None:
            file_path = ROOT_PATH / "support/files/map_sections.txt"
        with open(file_path, "r") as file:
            for line in file:
                # Strip any leading/trailing whitespace and split the line by commas
                values = line.strip().split(',')
                # Convert values to floats
                min_lon, min_lat, max_lon, max_lat = map(float, values)
                # Yield as tuples of (longitude range, latitude range)
                yield min_lon, max_lon, min_lat, max_lat
    
    @staticmethod
    def replace_coordinates_with_placeholders(url: str) -> str:
    # Define the regex pattern to match the coordinate parameters
        pattern = (
            r"(minLon=)(-?\d+\.?\d*)&"
            r"(minLat=)(-?\d+\.?\d*)&"
            r"(maxLon=)(-?\d+\.?\d*)&"
            r"(maxLat=)(-?\d+\.?\d*)&"
        )
        # Replace the matched values with placeholders
        replaced_url = re.sub(
            pattern,
            r"\1{minLon}&\3{minLat}&\5{maxLon}&\7{maxLat}&",
            url
        )
        return replaced_url

    # def read_map(self, file_path: Union[Path, str]):

    
