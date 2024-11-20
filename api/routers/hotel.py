from api.domain.hotel import service, schemas
from services.database import BaseDB
from .converter.hotel import convert
from .. import hotel_api

@hotel_api('/hotel')
def get_hotel(hotel_db: BaseDB, hotel_filter: schemas.HotelFilter):
    return convert(service.get_hotel(hotel_db, schemas.HotelFilter(**hotel_filter)))
