from datetime import datetime
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel


app = FastAPI()

# TODO - move to env variable
cluster = MongoClient('mongodb+srv://pologonz:hardtoguess@main.mks0e.mongodb.net/gh?retryWrites=true&w=majority')
db = cluster['gh']['users']

class User(BaseModel):
  name: str
  email: str
  zipcode: int
  _id: str = ''
  courses: list = []
  # created: datetime.date
  # updated: datetime.date = None

@app.get('/')
async def root():
  """ returns list of users' name and email """
  cursor = db.find()
  obj = {}
  for c in cursor:
    obj.update({str(c['_id']): [c['name'], c['email']]})
  return obj

@app.get('/user/{user_id}')
async def get_user(user_id):
  c = db.find_one({'name':user_id})
  return {str(c['_id']): [c['name'], c['email'], c['zip']]}

@app.put('/user/{user_id}')
async def update_user(user_id, obj):
  c = db.find_one_and_update({'name':user_id}, {'$set': obj})
  return {str(c['_id']): [c['name'], c['email']]}

@app.delete('/user/{user_id}')
async def delete_user(user_id):
  c = db.find_one_and_delete({'name':user_id})
  return {str(c['_id']): [c['name'], c['email'], c['zip']]}
