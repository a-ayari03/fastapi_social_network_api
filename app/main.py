from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel
from random import randrange

app = FastAPI() #uvicorn app.main:app --reload 

# title str, content str
class Post(BaseModel):
    """
    Pydantic model for schema validation for posting new 'post' requests
    """
    title : str 
    content : str
    published : bool = True
    rating : Optional[int] = None


my_post = [
    {'title': 'Top beaches in La Ciotat', 'content': 'check out this awesome beaches !', 'published': True, 'rating': None, 'id': 2}
    ,{'title': 'zzzz', 'content': 'check out this awesome beaches !', 'published': True, 'rating': None, 'id': 3}]

def find_post(id):
    for p in my_post :
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_post) :
        if p['id'] == id:
            return i
        
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data" : my_post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_post.append(post_dict)
    return {"data" : post_dict}

@app.get("/posts/latest") #
def get_latest_post():
    post = my_post[-1]
    return {'post_detail' : post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail= f'post with id : {id} does not exist' 
                             )
       # response.status_code = status.HTTP_404_NOT_FOUND # not post with specific id
       # return {'message' : f'post with id : {id} was not find'}
    
    return {'post_detail' : post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) :
    index = find_index_post(id)

    if index == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail= f'post with id : {id} does not exist'
                             )
    my_post.pop(index) 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):

    index = find_index_post(id)

    if index == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail= f'post with id : {id} does not exist'
                             )
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {'data' : post_dict}
