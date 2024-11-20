from pydantic import BaseModel


class HotelFilter(BaseModel):
    hotel_id: str
    destination_id: int = None