from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

# for CORS (Cross Origin Resource Sharing)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "https://www.google.com",
# ]

origins = ["*"] # if want to set up a public api, the origin will just be a wild card ["*"]

app.add_middleware(
    CORSMiddleware, # middleware is a common name in a lot of framework, its a function that run before every request
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favourite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

        
# path operation / route
@app.get("/")       # decorator (turn this into a path operation that someone who want to use the api can hit this end point) "/" is the root path
def read_root():    # function
    return {"Hello": "World"}

# got retrieving data use "get" method
@app.get("/posts")
def get_posts():
    return {"data": my_posts}
    # return {"data": "This is your posts"}

# changed @app.post("/createposts") to @app.post("/posts") for best practice
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post): # can put variable to be assigned data to (the variable name is payLoad, type dict, and equal to Body,)
    # its going to extract all of the field from body and convert it to python dictionary and store in in variable named payLoad
    # print(new_post.title)
    # print(new_post.content)
    # print(new_post.published)
    # print(new_post.rating)
    # print(new_post.model_dump())

    post_dict = new_post.model_dump()
    post_dict['id'] = randrange(0, 1000000)

    my_posts.append(new_post.model_dump())

    return {"data": post_dict}

# {id} represent path parameter
# Note: path parameters will always returned as a string, even though it may be an integer
@app.get("/posts/{id}")
def get_post(id: int, response: Response): # id:int fastapi will auto convert it to int type
    print(type(id))
    # post = find_post(int(id))
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} was not found.')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with id: {id} was not found.'}

    return{"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} doest not exists')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):   # post: Post is a schema from pydantic
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')
    
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

 




#title str, content str, category, Bool published post or draft



# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)): # can put variable to be assigned data to (the variable name is payLoad, type dict, and equal to Body,)
#     # its going to extract all of the field from body and convert it to python dictionary and store in in variable named payLoad
#     print(payLoad)
#     return {"new_post": f"title {payLoad['title']} content:{payLoad['content']}"}
# #title str, content str, category, Bool published post or draft

# @app.get("/virtualTryOn")
# def virtualTryOn():



    