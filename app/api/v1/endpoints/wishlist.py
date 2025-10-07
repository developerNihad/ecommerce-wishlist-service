from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models import Wishlist, WishlistCreate, WishlistResponse
from app.config import get_session

router = APIRouter()

@router.post("/wishlist", response_model=WishlistResponse)
def add_to_wishlist(
    wishlist: WishlistCreate, 
    session: Session = Depends(get_session)
):

    existing = session.exec(
        select(Wishlist).where(
            Wishlist.user_id == wishlist.user_id,
            Wishlist.product_variation_id == wishlist.product_variation_id
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This product already exists."
        )
    
    db_wishlist = Wishlist(**wishlist.dict())
    session.add(db_wishlist)
    session.commit()
    session.refresh(db_wishlist)
    
    return db_wishlist

@router.get("/wishlist/{user_id}", response_model=list[WishlistResponse])
def get_wishlist(user_id: int, session: Session = Depends(get_session)):

    wishlist_items = session.exec(
        select(Wishlist).where(Wishlist.user_id == user_id)
    ).all()
    
    return wishlist_items

@router.delete("/wishlist/{user_id}/{product_variation_id}")
def remove_from_wishlist(
    user_id: int, 
    product_variation_id: int, 
    session: Session = Depends(get_session)
):
    
    wishlist_item = session.exec(
        select(Wishlist).where(
            Wishlist.user_id == user_id,
            Wishlist.product_variation_id == product_variation_id
        )
    ).first()
    
    if not wishlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist item not found."
        )
    
    session.delete(wishlist_item)
    session.commit()
    
    return {"message": "Product deleted from wishlist."}