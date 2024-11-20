from . import models, schemas
from services.database import BaseDB


def get_hotel(db: BaseDB, hotel_filter: schemas.HotelFilter):
    try:
        data = db.find(hotel_filter.hotel_id, hotel_filter.destination_id)
        return models.HotelResponse(**data.model_dump())
    except Exception as e:
        return None
    
