from api.domain.hotels import service, schemas
from services.database import BaseDB
from .converter.hotels import convert

from .. import hotel_api

@hotel_api('/hotels')
def get_hotels(hotel_db: BaseDB, hotels_filter: schemas.HotelsFilter = {None, None}):
    return convert(service.get_hotels(hotel_db, schemas.HotelsFilter(**hotels_filter)))
