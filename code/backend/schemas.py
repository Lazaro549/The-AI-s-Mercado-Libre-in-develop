from pydantic import BaseModel
from typing import Dict, Optional

class ListingCreate(BaseModel):
    title: str
    description: str
    attributes: Dict[str, str] = {}

class Listing(ListingCreate):
    id: int
    price: Optional[float] = None

class PricePrediction(BaseModel):
    price: float
