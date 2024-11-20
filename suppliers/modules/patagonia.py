from suppliers.base_supplier import BaseSupplier
from models.hotel import Hotel, Location, Image, Amenities, HotelImages

class PatagoniaSupplier(BaseSupplier):
    @staticmethod
    def parse(data: dict) -> Hotel:
        location = Location(
            address = data.get("address"),
            # city = unknown field
            # country = unknown field
            # postal_code = unknown field
            latitude = data.get("lat"),
            longitude = data.get("lng")
        )
        images = HotelImages(
            rooms = [Image(link=image.get("url"), description = image.get("description")) for image in data.get('images').get("rooms")],
            amenities = [Image(link=image.get("url"), description = image.get("description")) for image in data.get('images').get("amenities")]
        )
        amenities = Amenities(
            general = data.get("amenities")
            # room = unknown field
        )
        hotel = Hotel(
            hotel_id = data.get("id"),
            destination_id = data.get("destination"),
            name = data.get("name"),
            description = data.get("info"),
            location = location,
            amenities = amenities,
            images = images,
            source = "patagonia"
        )
    
        return hotel