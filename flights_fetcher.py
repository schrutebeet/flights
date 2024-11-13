import re
from typing import List, Dict, Any, Union

import requests
from playwright.sync_api import sync_playwright

class FlightsFetcher:

    def __init__(self, webpage_url: str):
        self.webpage_url = webpage_url

    def run_all(self) -> None:
        url_calls_list = self.get_webpage_url_calls("vicinity_aircraft")
        token = self.get_aircraft_token(url_calls_list)
        for url in url_calls_list:
            result = self.get_json_from_api_call(url)


    def get_webpage_url_calls(self, filter_by: str) -> List[str]:
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
        header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'
            }
        s = requests.Session()
        s.headers.update(header)
        json_data = s.get(url).json()
        return json_data
