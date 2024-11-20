from services.database import HotelDB, RawHotelDB

# Initialize the raw hotel database
# This database is designed to store raw hotel data categorized by hotel ID and source.
raw_hotel_db = RawHotelDB()

# Initialize the hotel database
# This database holds processed or merged hotel data, indexed by hotel ID.
hotel_db = HotelDB()
