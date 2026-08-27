from typing import Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth
from ..database import getDb

# while True:
#     try:
#         connection = psycopg2.connect(host='localhost', database='pythonwebdev', user='postgres', password='admin', cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connection to PostgreSQL failed")
#         print("Error: ", error)
#         time.sleep(2)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[schemas.PostWithVotes])
async def getPosts(
    db: Session = Depends(getDb),
    currentUser: dict = Depends(oauth.getCurrentUser),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .order_by(models.Post.id.asc())
        .limit(limit)
        .offset(skip)
        .all()
    )
    return [{"Post": post, "votes": votes} for post, votes in results]


@router.get("/latest", response_model=schemas.PostResponse)
async def getLatestPost(
    db: Session = Depends(getDb), currentUser: dict = Depends(oauth.getCurrentUser)
):
    # cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    # post = cursor.fetchone()
    post = (
        db.query(models.Post)
        .filter(models.Post.user_id == currentUser.id)
        .order_by(models.Post.id.desc())
        .limit(1)
        .first()
    )
    return post


@router.get("/{id}", response_model=schemas.PostResponse)
async def getPost(
    id: int,
    response: Response,
    db: Session = Depends(getDb),
    currentUser: dict = Depends(oauth.getCurrentUser),
):
    # cursor.execute(f"SELECT * FROM posts WHERE id = {id}")
    # post = cursor.fetchone()
    # if post is None:
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message": "post not found"}
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # return {"data": post}

    post = (
        db.query(models.Post)
        .filter(models.Post.id == id, models.Post.user_id == currentUser.id)
        .first()
    )
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def createPosts(
    payload: schemas.CreatePost,
    db: Session = Depends(getDb),
    currentUser: dict = Depends(oauth.getCurrentUser),
):
    # postDict = payload.model_dump()
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ('{postDict['title']}', '{postDict['content']}', '{postDict['published']}') RETURNING *")
    # newPost = cursor.fetchone()
    # connection.commit()

    # newPost = models.Post(title=payload.title, content=payload.content, published=payload.published)
    # db.add(newPost)
    # db.commit()
    # db.refresh(newPost)
    # return {"data": newPost }
    newPost = models.Post(**payload.model_dump(), user_id=currentUser.id)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


@router.put("/{id}", response_model=schemas.PostResponse)
async def updatePost(
    id: int,
    payload: schemas.CreatePost,
    db: Session = Depends(getDb),
    currentUser: dict = Depends(oauth.getCurrentUser),
):
    # postDict = payload.model_dump()
    # cursor.execute(f"UPDATE posts SET title = '{postDict['title']}', content = '{postDict['content']}', published = '{postDict['published']}' WHERE id = {str(id)} RETURNING *")
    # updatedPost = cursor.fetchone()
    # connection.commit()
    # return {"data": updatedPost }

    postQuery = (
        db.query(models.Post)
        .filter(models.Post.id == id)
        .filter(models.Post.user_id == currentUser.id)
    )
    if postQuery.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    postQuery.update(payload.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(postQuery.first())
    return postQuery.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletePost(
    id: int,
    db: Session = Depends(getDb),
    currentUser: dict = Depends(oauth.getCurrentUser),
):
    # cursor.execute(f"DELETE FROM posts WHERE id = {str(id)}")
    # connection.commit()
    # if cursor.rowcount == 0:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    if post.first().user_id != currentUser.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
