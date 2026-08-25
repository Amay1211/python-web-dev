from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import getDb
from . import models
from typing import Annotated
from .config import settings

ALGORITHM = settings.jwt_algorithm
SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2Schema = OAuth2PasswordBearer(
    tokenUrl="/login"
)  # Token URL is for the swagger UI which shows the token input field


def createAccessToken(data: dict):
    toEncode = data.copy()
    expire = f"{datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}"
    toEncode.update({"expiryTimestamp": expire})
    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt


def verifyAccessToken(token: str, credentialsException: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userId = payload.get("user_id")
        if userId is None:
            raise credentialsException
        return userId
    except JWTError:
        raise credentialsException


def getCurrentUser(
    token: Annotated[str, Depends(oauth2Schema)], db: Session = Depends(getDb)
):
    userId = verifyAccessToken(
        token,
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ),
    )
    user = db.query(models.User).filter(models.User.id == userId).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
