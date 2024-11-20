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

class Hotel(BaseModel):
    hotel_id: str = Field(..., alias="Id")
    destination_id: int = Field(..., alias="DestinationId")
    name: str = Field(..., alias="Name")
    description: Optional[str] = None
    location: Location
    amenities: Optional[Amenities] = None
    images: Optional[HotelImages] = None  
    booking_conditions: Optional[List[str]] = None
    source: str = Field(..., alias="Source")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "hotel_id": "iJhz",
                "destination_id": 5432,
                "name": "Beach Villas Singapore",
                "description": "This 5 star hotel is located on the coastline of Singapore.",
                "location": {
                    "address": "8 Sentosa Gateway, Beach Villas",
                    "city": "Singapore",
                    "country": "SG",
                    "postal_code": "098269",
                    "latitude": 1.264751,
                    "longitude": 103.824006
                },
                "facilities": ["Pool", "BusinessCenter", "WiFi", "DryCleaning", "Breakfast"],
                "amenities": {
                    "general": ["outdoor pool", "business center", "childcare"],
                    "room": ["tv", "coffee machine", "kettle", "hair dryer", "iron"]
                },
                "images": {
                    "rooms": [
                        {
                            "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/2.jpg",
                            "caption": "Double room"
                        },
                        {
                            "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/3.jpg",
                            "caption": "Double room"
                        }
                    ],
                    "site": [
                        {
                            "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/1.jpg",
                            "caption": "Front"
                        }
                    ]
                },
                "booking_conditions": [
                    "All children are welcome.",
                    "Pets are not allowed.",
                    "WiFi is available in all areas and is free of charge."
                ]
            }
        }
