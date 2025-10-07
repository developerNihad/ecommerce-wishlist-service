from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Wishlist(SQLModel, table=True):
    __tablename__ = "wishlist"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    product_variation_id: int = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WishlistCreate(SQLModel):
    user_id: int
    product_variation_id: int

class WishlistResponse(SQLModel):
    id: int
    user_id: int
    product_variation_id: int
    created_at: datetime