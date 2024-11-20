from . import models, schemas
from services.database import BaseDB
from utils.logger import logger

def get_hotels(db: BaseDB, hotels_filter: schemas.HotelsFilter = {None, None}):
    try:
        data = db.find_all(hotels_filter.hotel_ids, hotels_filter.destination_ids)
        data = [models.HotelResponse(**hotel.model_dump()) for hotel in data]
        return models.HotelsResponse(hotels = data)
    except Exception as e:
        logger.log(f"Failed to get hotels: {e}", "error")
        return []
