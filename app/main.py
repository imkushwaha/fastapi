from fastapi import FastAPI, Response, status, HTTPException
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


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, P in enumerate(my_posts):
        if P["id"] == id:
            return i


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


# @app.get("/posts/{id}")  # {id} represents path parameter
# def get_post(id: int):
#     post = find_post(id)
#     return {"post_detail": post}


# Changing response status codes

# @app.get("/posts/{id}")  # {id} represents path parameter
# def get_post(id: int, response: Response):
#     post = find_post(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"post with id: {id} was not found"}
#     return {"post_detail": post}


# With HTTP Exception (same thing in much cleaner manner)

@app.get("/posts/{id}")  # {id} represents path parameter
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}


# Delete a post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting a post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

