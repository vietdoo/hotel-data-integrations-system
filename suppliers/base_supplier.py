import requests
from models.hotel import Hotel
from abc import ABC, abstractmethod
from typing import List
from utils.logger import logger


class BaseSupplier(ABC):
    def __init__(self, url: str):
        """
        Initialize the supplier with its API endpoint.

        :param url: API endpoint URL for the supplier
        """
        self._api_endpoint = url

    def _endpoint(self) -> str:
        """
        Get the supplier's API endpoint.

        :return: The API endpoint URL
        """
        return self._api_endpoint

    @abstractmethod
    def parse(self, data: dict) -> Hotel:
        """
        Parse a single item of supplier data into a Hotel object.

        :param data: A dictionary representing supplier data
        :return: A Hotel object
        """
        pass

    def fetch(self) -> List[Hotel]:
        """
        Fetch and parse data from the supplier's API endpoint.

        :return: A list of parsed Hotel objects
        """
        url = self._endpoint()
        logger.log(f"Fetching data from {url}", "info")

        # Attempt to fetch data
        try:
            response = requests.get(url)
        except requests.RequestException as e:
            logger.log(f"Request to {url} failed with error: {e}", "error")
            return []

        # Check HTTP response status
        if response.status_code != 200:
            logger.log(
                f"Failed to fetch data from {url} with status code {response.status_code}", "error")
            return []

        # Parse JSON response
        try:
            json_data = response.json()
        except Exception as e:
            logger.log(
                f"Failed to parse JSON response from {url} with error: {e}", "error")
            return []

        # Process each item in the response
        hotels = []
        for item in json_data:
            try:
                hotel = self.parse(item)
                hotels.append(hotel)
            except Exception as e:
                logger.log(
                    f"Failed to parse item from {url} with error: {e}", "error")

        return hotels
