from fastapi import FastAPI
from pymongo import MongoClient


app = FastAPI()

# TODO - move to env variable
cluster = MongoClient('mongodb+srv://pologonz:hardtoguess@main.mks0e.mongodb.net/gh?retryWrites=true&w=majority')
db = cluster['gh']['users']

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
async def update_user(user_id):
  c = db.find_one_and_update({'name':user_id}, {'$set': {'zip':75206}})
  return {str(c['_id']): [c['name'], c['email']]}

