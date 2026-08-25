from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import APIRouter
from .. import models, schemas, utils
from ..database import getDb
from .. oauth import createAccessToken

router = APIRouter(tags=["authentication"])

@router.post("/login", response_model=schemas.LoginResponse)
async def login(payload: schemas.Login, db: Session = Depends(getDb)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verifyPassword(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    accessToken = createAccessToken({"user_id": user.id})
    return {"accessToken": accessToken, "tokenType": "bearer"}