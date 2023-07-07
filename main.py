from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel  # To create a schem
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "favorite foods", "content": "I like pizza", "id": 2}]

@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/login")
def login_user():
    return {"message": "User logged in"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content: {payload['content']}"}


# @app.post("/posts")
# def create_posts(post: Post):
#     print(f"Title: {post.title}")
#     print(f"Content: {post.content}")
#     print(f"Published: {post.published}")
#     print(f"Rating: {post.rating}")
#     print(post.dict())  # convert pydantic model into dictionary
#     return {"data": post.dict()}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


@app.get("/posts/{id}")  # {id} represents path parameter
def get_post(id: int):
    post = find_post(id)
    return {"post_detail": post}



