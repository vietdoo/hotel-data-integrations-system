from services.normalizer import DataNormalizerInterface
from services.merger import BaseDataMerger
from services.database import RawHotelDB
from utils.logger import logger
from utils.exceptions import HotelServiceException


class HotelService:
    def __init__(self,
                 data,
                 normalizer: DataNormalizerInterface,
                 merger: BaseDataMerger,
                 raw_hotel_db: RawHotelDB = None):
        """
        Initialize the HotelService class with hotel data, normalizer, merger, and optional raw hotel database.
        """
        self.data = data
        self._normalizer = normalizer
        self._merger = merger
        self._raw_hotel_db = raw_hotel_db

    @property
    def get(self):
        """
        Retrieve the current hotel data.
        """
        return self.data

    def normalize_hotels(self):
        """
        Normalize hotel data using the provided normalizer.
        If a raw hotel database is available, update it with normalized data.
        """
        try:
            self.data = self._normalizer.normalize(self.data)
            logger.log(
                f"Successfully normalized {len(self.data)} hotels.", "info")
            if self._raw_hotel_db:
                self._update_raw_hotel_db()
        except Exception as e:
            logger.log(f"Error during normalization: {e}", "error")
            raise HotelServiceException(f"Normalization failed: {e}")

    def _update_raw_hotel_db(self):
        """
        Update the raw hotel database with normalized data.
        """
        try:
            for hotel in self.data:
                self._raw_hotel_db.update_one(hotel)
            logger.log(
                f"Updated raw hotel database with {len(self.data)} hotels.", "info")
        except Exception as e:
            logger.log(f"Failed to update raw hotel database: {e}", "error")
            raise HotelServiceException(
                f"Failed to update raw hotel database: {e}")

    def merge_hotels(self):
        """
        Merge hotels with the same ID. Uses the raw hotel database if available.
        """
        try:
            hotels_map_by_id = self._group_hotels_by_id()
            if self._raw_hotel_db:
                self._merge_hotels_with_db(hotels_map_by_id)
            else:
                self._merge_hotels_without_db(hotels_map_by_id)
            logger.log(
                f"Successfully merged hotels. Total merged hotels: {len(self.data)}.", "info")
        except Exception as e:
            logger.log(f"Error during merging: {e}", "error")
            raise HotelServiceException(f"Merging failed: {e}")

    def _group_hotels_by_id(self):
        """
        Group hotels by their unique ID into a dictionary.
        """
        hotels_map_by_id = {}
        for hotel in self.data:
            if hotel.hotel_id not in hotels_map_by_id:
                hotels_map_by_id[hotel.hotel_id] = [hotel]
            else:
                hotels_map_by_id[hotel.hotel_id].append(hotel)
        return hotels_map_by_id

    def _merge_hotels_with_db(self, hotels_map_by_id):
        """
        Merge hotels with existing data from the raw hotel database.
        """
        merged_data = []
        try:
            for hotel_id, hotels in hotels_map_by_id.items():
                merge_batch = []
                existing_hotels = self._raw_hotel_db.find_all([hotel_id])
                if existing_hotels:
                    merge_batch.extend(existing_hotels)
                logger.log(
                    f"Found {len(merge_batch)} existing hotels for ID {hotel_id}.", "info")
                merged_result = self._merger.merge(merge_batch)
                if merged_result:
                    merged_data.append(merged_result)

            self.data = merged_data
        except Exception as e:
            logger.log(f"Error merging hotels with DB: {e}", "error")
            raise HotelServiceException(f"Error merging hotels with DB: {e}")

    def _merge_hotels_without_db(self, hotels_map_by_id):
        """
        Merge hotels without using the raw hotel database.
        """
        merged_data = []
        try:
            for hotel_id, hotels in hotels_map_by_id.items():
                merged_result = self._merger.merge(hotels)
                if merged_result:
                    merged_data.append(merged_result)

            self.data = merged_data
        except Exception as e:
            logger.log(f"Error merging hotels without DB: {e}", "error")
            raise HotelServiceException(
                f"Error merging hotels without DB: {e}")
