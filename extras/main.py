from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Body, Depends
from random import randrange
import psycopg2
import utils
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db
from routers import post, user

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to my api !!!"}


# Matches the First Path Operation
@app.get("/")
def get_posts():
    return {"data": "This is your posts"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # curr.execute(""" SELECT * FROM posts""")
    # posts = curr.fetchall()
    # return {"data": posts}
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # curr.execute(
    #     """ INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,
    #     (
    #         post.title,
    #         post.content,
    #         post.published,
    #     ),
    # )

    # conn.commit()

    new_post = models.Post(**post.model_dump())

    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published
    # )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # new_post = curr.fetchone()
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, resposne: Response, db: Session = Depends(get_db)):

    # curr.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = curr.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found"
        )

    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # curr.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = curr.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} doesnt exist",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    update_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = update_query.first()

    # curr.execute(
    #     """ UPDATE posts SET title = %s, content=%s, published=%s WHERE id =%s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # )

    # updated_post = curr.fetchone()
    # conn.commit()

    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} doesnt exist",
        )

    update_query.update(
        post.model_dump(),
        synchronize_session=False,
    )

    db.commit()

    return update_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} doesn't exist",
        )

    return user


# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):
#     # query = db.query(models.Post)
#     posts = db.query(models.Post).all()
#     return {"data": posts}


# my_posts = [
#     {"title": "title of post 1", "content": "content of post 1", "id": 1},
#     {"title": "favirte food", "content": "i like pizza", "id": 2},
# ]


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     # rating: Optional[int] = None


# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="root",
#             cursor_factory=RealDictCursor,
#         )
#         curr = conn.cursor()
#         print("The Database connection is successful")
#         break
#     except Exception as err:
#         print("Database conn failed")
#         print("Error:", err)
#         time.sleep(2)


# def find_posts(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i


# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):
#     # query = db.query(models.Post)
#     posts = db.query(models.Post).all()
#     return {"data": posts}


# @app.get("/")
# def root():
#     return {"message": "Welcome to my api !!!"}


# # Matches the First Path Operation
# @app.get("/")
# def get_posts():
#     return {"data": "This is your posts"}


# @app.get("/posts")
# def get_posts():
#     curr.execute(""" SELECT * FROM posts""")
#     posts = curr.fetchall()
#     return {"data": posts}


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     curr.execute(
#         """ INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,
#         (
#             post.title,
#             post.content,
#             post.published,
#         ),
#     )

#     conn.commit()

#     new_post = curr.fetchone()
#     # post_dict = post.model_dump()
#     # post_dict["id"] = randrange(0, 10000000)
#     # my_posts.append(post_dict)
#     return {"data": new_post}


# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     # print(post)
#     # print(post.dict())
#     # print(post.model_dump())
#     return {"new_post": f"title:{payLoad['title']}, content:{payLoad['content']}"}


# @app.get("/posts/{id}")
# def get_post(id: int, resposne: Response):

#     curr.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
#     post = curr.fetchone()
#     # post = find_posts(id)
#     if not post:
#         raise HTTPException(
#             status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found"
#         )
#         # resposne.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message":f"post with id {id} was not found"}
#     return {"post_detail": post}


# # This gives raise in to an error
# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return {"detail": post}


# @app.get("/posts/recent/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return {"detail": post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     curr.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#     deleted_post = curr.fetchone()
#     # index = find_index_post(id)
#     conn.commit()
#     if deleted_post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with id {id} doesnt exist",
#         )
#     # my_posts.pop(index)
#     return Response(
#         status_code=status.HTTP_204_NO_CONTENT
#     )  # {"message": "post was succesfully deleted"}


# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):

#     curr.execute(
#         """ UPDATE posts SET title = %s, content=%s, published=%s WHERE id =%s RETURNING *""",
#         (post.title, post.content, post.published, str(id)),
#     )

#     updated_post = curr.fetchone()
#     conn.commit()

#     # index = find_index_post(id)
#     if updated_post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with id {id} doesnt exist",
#         )

#     # post_dict = post.model_dump()
#     # post_dict["id"] = id
#     # my_posts[index] = post_dict

#     return {"data": updated_post}
