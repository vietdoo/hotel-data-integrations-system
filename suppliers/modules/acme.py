from suppliers.base_supplier import BaseSupplier
from models.hotel import Hotel, Location, Image, Amenities, HotelImages

class AcmeSupplier(BaseSupplier):
    @staticmethod
    def parse(data: dict) -> Hotel:
        location = Location(
            address = data.get("Address"),
            city = data.get("City"),
            country = data.get("Country"),
            postal_code = data.get("PostalCode"),
            latitude = data.get("Latitude"),
            longitude = data.get("Longitude")
        )
        amenities = Amenities(
            general = data.get("Facilities"),
            room = []
        )
        hotel = Hotel(
            hotel_id = data.get("Id"),
            destination_id = data.get("DestinationId"),
            name = data.get("Name"),
            description = data.get("Description"),
            location = location,
            amenities = amenities,
            source = "acme",
            # booking_conditions = data.get("BookingConditions")
        )
        return hotel
       
    