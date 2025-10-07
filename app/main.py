from fastapi import FastAPI
from app.config import create_db_and_tables
from app.api.v1.endpoints import wishlist
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    create_db_and_tables()
    yield

app = FastAPI(
    title="Wishlist Service",
    description="Wishlist Microservice",
    lifespan=lifespan
)

app.include_router(wishlist.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Wishlist Service working"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}