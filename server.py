from fastapi import FastAPI
from pymongo import MongoClient


app = FastAPI()

# TODO - move to env variable
cluster = MongoClient('mongodb+srv://pologonz:hardtoguess@main.mks0e.mongodb.net/gh?retryWrites=true&w=majority')
db = cluster['gh']['users']

@app.get('/')
async def root():
  cursor = db.find()
  lst = []
  for c in cursor:
    lst.append(c['_id'])
  print(type(lst[0]))
  return {"message": "Hello World", "otherkey":1, 3:'othervalue'}

@app.get('/user/{user_id}')
async def read_user(user_id):
  return {'user id': user_id}
