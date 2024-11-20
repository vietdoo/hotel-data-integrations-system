from abc import ABC, abstractmethod
import re
from utils.logger import logger
from utils.exceptions import CleanerException

class Cleaner(ABC):
    @abstractmethod
    def clean_text(self, text: str) -> str:
        """
        Clean raw text data by removing unwanted characters and formatting.

        :param text: The text to be cleaned
        :return: The cleaned text
        """
        pass

    @abstractmethod
    def clean_caption(self, text: str) -> str:
        """
        Clean caption text for consistency and lowercase formatting.

        :param text: The caption text to be cleaned
        :return: The cleaned caption
        """
        pass

    @abstractmethod
    def clean_amenity(self, text: str) -> str:
        """
        Clean amenity text, including splitting by capital letters and formatting.

        :param text: The amenity text to be cleaned
        :return: The cleaned amenity text
        """
        pass


class HotelCleaner(Cleaner):
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean general text by removing unwanted characters and whitespace.

        - Removes non-alphanumeric characters (except for spaces and basic punctuation)
        - Strips excessive whitespace and trims spaces around punctuation.

        :param text: The text to be cleaned
        :return: The cleaned text
        """
        if not isinstance(text, str):
            logger.log("Cleaner: Invalid input: text must be a string", "warning")
            return ""

        # Replace non-alphanumeric characters (except spaces, punctuation) with space
        pattern = r'[^a-zA-Z0-9\s.,"\'?!]'
        text = re.sub(pattern, ' ', text)

        # Remove spaces before punctuation
        text = re.sub(r'\s([^\w\s])', r'\1', text)

        # Remove extra spaces
        text = ' '.join(text.split())

        # Trim leading/trailing whitespace
        text = text.strip()

        return text

    def clean_caption(self, text: str) -> str:
        """
        Clean caption text by:
        - Applying general cleaning
        - Lowercasing the cleaned text

        :param text: The caption text to be cleaned
        :return: The cleaned caption text
        """
        if not isinstance(text, str):
            logger.log('Cleaner: Invalid input: caption text must be a string', 'warning')
            return ""

        # Clean text using the clean_text method
        text = self.clean_text(text)

        # Convert text to lowercase
        text = text.lower()

        return text

    def clean_amenity(self, text: str) -> str:
        """
        Clean amenity text by:
        - Applying general cleaning
        - Splitting by capital letters and converting to lowercase.

        :param text: The amenity text to be cleaned
        :return: The cleaned amenity text
        """
        if not isinstance(text, str):
            logger.log("Cleaner: Invalid input: amenity text must be a string", "warning")
            return ""

        # Clean text using the clean_text method
        text = self.clean_text(text)

        # Split by capital letters (except at the start of the string)
        text = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)

        # Convert to lowercase
        text = text.lower()

        return text
