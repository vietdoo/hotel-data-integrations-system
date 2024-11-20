from . import schemas, repository


def get_hotel(db, hotel_filter: schemas.HotelFilter):
    return repository.get_hotel(db, hotel_filter)
