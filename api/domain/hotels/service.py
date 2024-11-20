from . import schemas, repository


def get_hotels(db, hotels_filter: schemas.HotelsFilter = {None, None}):
    return repository.get_hotels(db, hotels_filter)
