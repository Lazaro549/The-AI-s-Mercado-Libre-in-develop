from fastapi import FastAPI, HTTPException
from typing import List
from models import predict_price
from schemas import ListingCreate, Listing, PricePrediction
from store import STORE, next_id

app = FastAPI(title="AI Mercado Libre (dev)")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/listings", response_model=Listing)
def create_listing(l: ListingCreate):
    id = next_id()
    listing = Listing(id=id, **l.dict())
    STORE.append(listing)
    return listing

@app.get("/listings", response_model=List[Listing])
def list_listings():
    return STORE

@app.post("/predict", response_model=PricePrediction)
def predict(l: ListingCreate):
    price = predict_price(l.title, l.description, l.attributes)
    return PricePrediction(price=price)
