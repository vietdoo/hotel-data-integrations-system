from models.hotel import Hotel
from abc import ABC, abstractmethod
from typing import List, Optional
from utils.exceptions import DBException
from utils.logger import logger


class BaseDB(ABC):
    def __init__(self) -> None:
        """
        Base database class to define the common interface for database operations.
        """
        self._length = 0

    @abstractmethod
    def update_one(self, hotel: Hotel) -> Optional[Hotel]:
        """
        Update a single hotel record in the database.
        """
        pass
    
    @abstractmethod
    def update_many(self, hotels: List[Hotel]) -> Optional[List[Hotel]]:
        """
        Update multiple hotel records in the database.
        """
        pass
    
    @abstractmethod
    def find(self, hotel_id: str, destination_id: Optional[str]) -> Optional[Hotel]:
        """
        Find a single record of a hotel by its ID.
        """
        pass

    @abstractmethod
    def find_all(self, hotel_ids: Optional[List[str]], destination_ids: Optional[List[str]]) -> Optional[List[Hotel]]:
        """
        Find multiple records of hotels by their IDs matching the given destination IDs.
        """
        pass

    def length(self) -> int:
        """
        Get the total number of records in the database.
        """
        return self._length


class HotelDB(BaseDB):
    """
    A simple database to store unique hotels by their ID.
    """

    def __init__(self):
        super().__init__()
        self.data: dict[str, Hotel] = {}

    def update_one(self, hotel: Hotel) -> Hotel:
        """
        Add or update a hotel record. If the hotel ID is new, increase the count.
        """
        if hotel.hotel_id not in self.data:
            self._length += 1
        self.data[hotel.hotel_id] = hotel
        logger.log(f"Updated HotelDB with hotel ID {hotel.hotel_id}.", "info")
        return hotel
    
    def update_many(self, hotels: List[Hotel]) -> List[Hotel]:
        """
        Add or update multiple hotel records.
        """
        for hotel in hotels:
            self.update_one(hotel)
        return hotels

    def find_all(self, hotel_ids: Optional[List[str]], destination_ids: Optional[List[str]]) -> Optional[List[Hotel]]:
        """
        Retrieve all hotels with the given ID.
        """
        if not hotel_ids or not destination_ids:
            return list(self.data.values())

        hotel_ids = set(hotel_ids)
        destination_ids = set(destination_ids)
        
        try:
            hotels = []
            
            for hotel_id in hotel_ids:
                hotel = self.find(hotel_id)
                if hotel and hotel.destination_id in destination_ids:
                    hotels.append(hotel)
            
            return hotels
    
        except Exception as e:
            logger.log(f"Failed to find hotels in HotelDB: {e}", "error")
            raise DBException(f"Error finding hotels in HotelDB: {e}")  


    def find(self, hotel_id, destination_id = None) -> Optional[Hotel]:
        """
        Retrieve a single hotel by its ID.
        """
        if destination_id:
            logger.log(f"Searching for hotel ID {hotel_id} in HotelDB with destination ID {destination_id}.", "info")
            return self.find_by_id_and_destination(hotel_id, destination_id)
        
        hotel = self.data.get(hotel_id, None)
        if hotel:
            logger.log(f"Found hotel ID {hotel_id} in HotelDB.", "info")
        else:
            logger.log(f"Hotel ID {hotel_id} not found in HotelDB.", "warning")
            
        return hotel
    
    def find_by_id_and_destination(self, hotel_id: str, destination_id: str) -> Optional[Hotel]:
        """
        Retrieve a single hotel by its ID.
        """
        hotel = self.data.get(hotel_id, None)
        
        if not hotel:
            logger.log(f"Hotel ID {hotel_id} not found in HotelDB.", "warning")
            return None
        
        if hotel.destination_id != destination_id:
            logger.log(f"Hotel ID {hotel_id} does not match destination ID {destination_id}.", "warning")
            return None
            
        return hotel
        


class RawHotelDB(BaseDB):
    """
    A database for storing raw hotel data from multiple sources.
    """

    def __init__(self):
        super().__init__()
        self.data: dict[str, dict[str, Hotel]] = {}

    def update_one(self, hotel: Hotel) -> Hotel:
        """
        Add or update a raw hotel record. Tracks multiple sources for the same hotel ID.
        """
        try:
            if hotel.hotel_id in self.data:
                if hotel.source not in self.data[hotel.hotel_id]:
                    self._length += 1
                self.data[hotel.hotel_id][hotel.source] = hotel
            else:
                self.data[hotel.hotel_id] = {hotel.source: hotel}
                self._length += 1
            logger.log(
                f"Updated RawHotelDB with hotel ID {hotel.hotel_id} from source {hotel.source}.", "info")
            return hotel
        except Exception as e:
            logger.log(f"Failed to update RawHotelDB: {e}", "error")
            raise DBException(f"Error updating RawHotelDB: {e}")
    
    def update_many(self, hotels: List[Hotel]) -> List[Hotel]:
        """
        Add or update multiple raw hotel records.
        """
        for hotel in hotels:
            self.update_one(hotel)
        return hotels
    
    def find(self, hotel_id: str, destination_id = None) -> Optional[Hotel]:
        """
        Retrieve a single hotel record for the given ID across all sources.
        """
        try:
            if destination_id:
                logger.log(f"Searching for hotel ID {hotel_id} in RawHotelDB with destination ID {destination_id}.", "info")
                # return self.find_by_id_and_destination(hotel_id, destination_id)
                return None
            
            if hotel_id in self.data:
                logger.log(
                    f"Found {len(self.data[hotel_id])} entries for hotel ID {hotel_id} in RawHotelDB.", "info")
                return list(self.data[hotel_id].values())[0]
            logger.log(
                f"No entries found for hotel ID {hotel_id} in RawHotelDB.", "warning")
            return None
        except Exception as e:
            logger.log(
                f"Failed to find entries in RawHotelDB for hotel ID {hotel_id}: {e}", "error")
            raise DBException(
                f"Error finding entries for hotel ID {hotel_id}: {e}")

    def find_all(self, hotel_ids: Optional[List[str]] = [], destination_ids: Optional[List[str]] = None) -> Optional[List[Hotel]]:
        
        
        if not hotel_ids:
            return []
        
        """
        Retrieve all hotel records for the given ID across all sources.
        """
        hotels = []
        
        try:
            for hotel_id in hotel_ids:
                if hotel_id in self.data:
                    logger.log(
                        f"Found {len(self.data[hotel_id])} entries for hotel ID {hotel_id} in RawHotelDB.", "info")
                    hotels.extend(list(self.data[hotel_id].values()))
                logger.log(
                    f"No entries found for hotel ID {hotel_id} in RawHotelDB.", "info")
            return hotels
        
        except Exception as e:
            logger.log(
                f"Failed to find entries in RawHotelDB for hotel ID {hotel_id}: {e}", "error")
            raise DBException(
                f"Error finding entries for hotel ID {hotel_id}: {e}")
