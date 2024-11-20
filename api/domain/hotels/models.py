from typing import List, Optional, Dict
from pydantic import BaseModel, field_validator, Field, HttpUrl


class Image(BaseModel):
    link: HttpUrl
    description: Optional[str] = None


class Amenities(BaseModel):
    general: Optional[List[str]] = None
    room: Optional[List[str]] = None


class Location(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator('*', mode='before')
    def empty_string_to_none(cls, v):
        return None if v == '' else v


class HotelImages(BaseModel):
    rooms: Optional[List[Image]] = None
    site: Optional[List[Image]] = None
    amenities: Optional[List[Image]] = None


class HotelResponse(BaseModel):
    hotel_id: str = Field(..., alias="Id")
    destination_id: int = Field(..., alias="DestinationId")
    name: str = Field(..., alias="Name")
    description: Optional[str] = None
    location: Location
    amenities: Optional[Amenities] = None
    images: Optional[HotelImages] = None
    booking_conditions: Optional[List[str]] = None

    class Config:
        populate_by_name = True

class HotelsResponse(BaseModel):
    hotels: List[HotelResponse]
    # count: int
    # page: int
    # total_pages: int
    # total_count: int

    class Config:
        populate_by_name = True