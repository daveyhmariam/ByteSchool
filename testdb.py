#!/usr/bin/env python3

from backend.models.user import User
from pymongo import MongoClient


client = MongoClient("localhost", 27017)
db = client['ByteSchool']
collection = db["proj_catalog"]
ctnt = collection.find()
c = ''

"""
document = ctnt[0]
with open("t2.txt", 'w') as f:
    f.write(document["tasks"][0]["checkers"][1]["correction_code"])
    """

with open("proj_catalog.json", 'r') as f:
    import json
    d = json.load(f)
    collection.insert_one(d)

collection = db["User"]
arg = {
    "username": "daniel",
    "email": "danielY@exam.com",
    "curriculum": "",
    "user_github": "",
    "password": "securepassword123",
    "role": "admin"
}
user = User(**arg)
