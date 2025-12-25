from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    parcels,
    listings,
    customers,
    offers,
    analysis,
    ai,
    drone,
    locations
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(parcels.router, prefix="/parcels", tags=["Parcels"])
api_router.include_router(listings.router, prefix="/listings", tags=["Listings"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(offers.router, prefix="/offers", tags=["Offers"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI"])
api_router.include_router(drone.router, prefix="/drone", tags=["Drone Tour"])
api_router.include_router(locations.router, prefix="/locations", tags=["Locations"])

