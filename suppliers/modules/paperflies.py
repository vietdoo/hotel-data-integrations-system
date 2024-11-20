from suppliers.base_supplier import BaseSupplier
from models.hotel import Hotel, Location, Image, Amenities, HotelImages

class PaperfliesSupplier(BaseSupplier):
    @staticmethod
    def parse(data: dict) -> Hotel:
        location = Location(
            address = data.get("location").get("address"),
            # city = unknown field
            country = data.get("location").get("country"),
            # postal_code = unknown field
            # latitude = unknown field
            # longitude = unknown field
        )
        images = HotelImages(
            rooms = [Image(link = image.get("link"), description = image.get("caption")) for image in data.get("images").get("rooms")],
            site = [Image(link = image.get("link"), description = image.get("caption")) for image in data.get("images").get("site")]
        )
        amenities = Amenities(
            general = data.get("amenities").get("general"),
            room = data.get("amenities").get("room")
        )
    
        hotel = Hotel(
            hotel_id = data.get("hotel_id"),
            destination_id = data.get("destination_id"),
            name = data.get("hotel_name"),
            description=data.get("details"),
            location = location,
            amenities = amenities,
            images = images,
            booking_conditions = data.get("booking_conditions"),
            source = "paperflies"
        )
        
        return hotel