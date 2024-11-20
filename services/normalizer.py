from typing import List, Any, TypeVar
from abc import ABC, abstractmethod
from models.hotel import Hotel, Location, Amenities, HotelImages
from utils.cleaner import Cleaner
from utils.exceptions import NormalizerException
from utils.logger import logger

class DataNormalizerInterface(ABC):
    @abstractmethod
    def normalize(self, data: List[Any]) -> List[Any]:
        """Normalize hotel data"""


T = TypeVar('T')


class AttributeNormalizer(ABC):
    def __init__(self, cleaner: Cleaner):
        self.cleaner = cleaner

    @abstractmethod
    def normalize(self, data: T) -> T:
        """Normalize hotel attribute"""


class DataNormalizer(DataNormalizerInterface):
    def __init__(self, normalizers: dict[str, AttributeNormalizer]):
        self.normalizers = normalizers

    def normalize(self, data: List[Hotel]) -> List[Hotel]:
        for hotel in data:
            logger.log(f"Normalizing hotel {hotel.hotel_id} {hotel.source}", "info")
            for field, normalizer in self.get_all_normalizers():
                if hasattr(hotel, field):
                    try:
                        setattr(hotel, field, normalizer.normalize(
                            getattr(hotel, field)))
                    except Exception as e:
                        raise NormalizerException(
                            f"Error normalizing field '{field}' of hotel '{hotel}'") from e
        return data

    def get_all_normalizers(self):
        return self.normalizers.items()


class NameNormalizer(AttributeNormalizer):
    def normalize(self, data: str) -> str:
        """Normalize the name field"""
        try:
            if not data:
                return data
            # Clean the name field using the cleaner
            return self.cleaner.clean_text(data)
        except Exception as e:
            raise NormalizerException(
                f"Error normalizing name: {data}") from e


class DescriptionNormalizer(AttributeNormalizer):
    def normalize(self, data: str) -> str:
        """Normalize the description field"""
        try:
            return self.cleaner.clean_text(data)
        except Exception as e:
            raise NormalizerException(
                f"Error normalizing description: {data}") from e


class LocationNormalizer(AttributeNormalizer):
    def normalize(self, data: Location) -> Location:
        """Normalize the location field."""
        try:
            if not data:
                return data

            # Clean the location fields
            if hasattr(data, "address") and data.address:
                data.address = self.cleaner.clean_text(data.address)
            if hasattr(data, "city") and data.city:
                data.city = self.cleaner.clean_text(data.city)
            if hasattr(data, "country") and data.country:
                data.country = self.cleaner.clean_text(data.country)
            if hasattr(data, "postal_code") and data.postal_code:
                data.postal_code = self.cleaner.clean_text(data.postal_code)

            return data
        except Exception as e:
            raise NormalizerException(
                f"Error normalizing location: {data}") from e


class AmenitiesNormalizer(AttributeNormalizer):
    def normalize(self, data: Amenities) -> Amenities:
        """Normalize the amenities field."""
        try:
            if not data:
                return data

            if hasattr(data, "general") and data.general:
                data.general = [self.cleaner.clean_amenity(
                    amenity) for amenity in data.general]

            if hasattr(data, "room") and data.room:
                data.room = [self.cleaner.clean_amenity(
                    amenity) for amenity in data.room]

            return data
        except Exception as e:
            raise NormalizerException(
                f"Error normalizing amenities: {data}") from e


class ImagesNormalizer(AttributeNormalizer):
    def normalize(self, data: HotelImages) -> HotelImages:
        """Normalize the images field."""
        try:
            if not data:
                return data

            # Clean the images fields
            if hasattr(data, "rooms") and data.rooms:
                for image in data.rooms:
                    if hasattr(image, "caption") and image.caption:
                        image.caption = self.cleaner.clean_caption(
                            image.caption)
            if hasattr(data, "amenities") and data.amenities:
                for image in data.amenities:
                    if hasattr(image, "caption") and image.caption:
                        image.caption = self.cleaner.clean_caption(
                            image.caption)
            return data
        except Exception as e:
            raise NormalizerException(
                f"Error normalizing images: {data}") from e


class BookingConditionsNormalizer(AttributeNormalizer):
    def normalize(self, data: list[str]) -> list[str]:
        """Normalize the booking_conditions field"""
        try:
            if not data:
                return data
            return [self.cleaner.clean_text(condition) for condition in data]
        except Exception as e:
            raise NormalizerException(
                f"Error normalizing booking conditions: {data}") from e
