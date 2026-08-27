from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import getDb
from ..oauth import getCurrentUser

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    payload: schemas.Vote,
    db: Session = Depends(getDb),
    currentUser: dict = Depends(getCurrentUser),
):
    post = db.query(models.Post).filter(models.Post.id == payload.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )

    if payload.dir == 1:
        userQuery = db.query(models.Vote).filter(
            models.Vote.post_id == payload.post_id,
            models.Vote.user_id == currentUser.id,
        )
        if userQuery.first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="vote already exists"
            )
        newVote = models.Vote(post_id=payload.post_id, user_id=currentUser.id)
        db.add(newVote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        userQuery = db.query(models.Vote).filter(
            models.Vote.post_id == payload.post_id,
            models.Vote.user_id == currentUser.id,
        )
        if not userQuery.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist"
            )
        userQuery.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
