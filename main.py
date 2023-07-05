from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel  # To create a schem
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/login")
def login_user():
    return {"message": "User logged in"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content: {payload['content']}"}


@app.post("/createposts")
def create_post(post: Post):
    print(f"Title: {post.title}")
    print(f"Content: {post.content}")
    print(f"Published: {post.published}")
    print(f"Rating: {post.rating}")
    print(post.dict())  # convert pydantic model into dictionary
    return {"data": post.dict()}