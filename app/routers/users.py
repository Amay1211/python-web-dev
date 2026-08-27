from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import getDb

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def createUser(payload: schemas.CreateUser, db: Session = Depends(getDb)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    payloadModel = payload.model_dump()
    payloadModel["password"] = utils.hashPassword(payloadModel["password"])
    userModel = models.User(**payloadModel)
    db.add(userModel)
    db.commit()
    db.refresh(userModel)
    return userModel


@router.get("/{id}", response_model=schemas.UserResponse)
async def getUser(id: int, db: Session = Depends(getDb)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )
    return user
