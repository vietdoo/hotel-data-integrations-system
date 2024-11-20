from pydantic import BaseModel
from typing import List, Optional, Dict

class HotelsFilter(BaseModel):
    hotel_ids: Optional[List[str]] = None
    destination_ids: Optional[List[int]] = None
    