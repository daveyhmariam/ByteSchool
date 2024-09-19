#!/usr/bin/python3
"""
Contains the MongoDBStorage class
"""

from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from backend.models.checker import Checker
from backend.models.file_checker import FileChecker
from backend.models.code_checker import CodeChecker
from backend.models.task import Task
from backend.models.project import Project
from backend.models.user import User
import uuid
import os


classes = {
    'Checker': Checker,
    'FileChecker': FileChecker,
    'CodeChecker': CodeChecker,
    'Task': Task,
    'Project': Project,
    'User': User,
}

class MongoDBStorage:
    """Interacts with MongoDB database"""

    def __init__(self):
        """Instantiate a MongoDBStorage object"""
        # Connection to MongoDB
        self.client = MongoClient(os.getenv('MONGO_HOST', 'localhost'), 27017)
        self.db = self.client[os.getenv('MONGO_DB', 'ByteSchool')]

    def all(self, cls=None):
        """Returns a dictionary of all objects of a class, or all objects"""
        result = {}
        if cls:
            collection = self.db[cls.__name__]
            documents = collection.find()
            for doc in documents:
                obj = classes[cls.__name__](**doc)
                obj._id = str(doc['_id'])  # Convert ObjectId to string
                result[cls.__name__ + '.' + str(doc['_id'])] = obj
        else:
            # Get all classes
            for class_name in classes:
                collection = self.db[class_name]
                documents = collection.find()
                for doc in documents:
                    obj = classes[class_name](**doc)
                    obj._id = str(doc['_id'])  # Convert ObjectId to string
                    result[class_name + '.' + str(doc['_id'])] = obj
        return result

    def new(self, obj):
        """Inserts a new object into the MongoDB collection"""
        if obj:
            collection = self.db[obj.__class__.__name__]
            obj_dict = obj.to_dict()
            
            # Ensure _id is an ObjectId
            if '_id' in obj_dict:
                if isinstance(obj_dict['_id'], str):
                    try:
                        obj_dict['_id'] = ObjectId(obj_dict['_id'])
                    except Exception as e:
                        print(f"Failed to convert _id to ObjectId: {e}")
                        return
                elif isinstance(obj_dict['_id'], uuid.UUID):
                    obj_dict['_id'] = ObjectId.from_uuid(obj_dict['_id'])

            try:
                # Insert into MongoDB
                collection.insert_one(obj_dict)
                obj._id = str(obj_dict['_id'])  # Convert ObjectId to string for the object
            except errors.DuplicateKeyError:
                # Update if a duplicate key error occurs
                collection.update_one(
                    {'_id': obj_dict['_id']},
                    {'$set': obj_dict}
                )

    def save_object(self, obj):
        """Updates an existing object in the MongoDB collection"""
        if obj:
            collection = self.db[obj.__class__.__name__]
            obj_dict = obj.to_dict()

            # Ensure _id is an ObjectId
            if '_id' in obj_dict:
                if isinstance(obj_dict['_id'], str):
                    try:
                        obj_dict['_id'] = ObjectId(obj_dict['_id'])
                    except Exception as e:
                        print(f"Failed to convert _id to ObjectId: {e}")
                        return
                elif isinstance(obj_dict['_id'], uuid.UUID):
                    obj_dict['_id'] = ObjectId.from_uuid(obj_dict['_id'])

            try:
                result = collection.update_one(
                    {"_id": obj_dict["_id"]},
                    {"$set": obj_dict},
                    upsert=True  # Insert the document if it does not exist
                )
                if result.matched_count == 0:
                    print("Document not found, created new document.")
                else:
                    print("Document updated successfully.")
            except Exception as e:
                print(f"Error updating object: {e}")

    def delete(self, obj=None):
        """Deletes an object from MongoDB collection"""
        if obj:
            collection = self.db[obj.__class__.__name__]
            collection.delete_one({"_id": ObjectId(obj._id)})


    def close(self):
        """Close the MongoDB connection"""
        self.client.close()

    def get(self, cls, id):
        """Returns the object based on the class name and its ID"""
        if cls not in classes.keys():
            print("classes", cls)
            print(classes.keys())
            print("retrun none get mongo")
            return None
        collection = self.db[cls]
        doc = collection.find_one({"_id": ObjectId(id)})
        if doc:
            obj = classes[cls](**doc)
            obj._id = str(doc['_id'])  # Convert ObjectId to string
            return obj
        print("retrun none get mongo outer")
        return None

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls:
            collection = self.db[cls.__name__]
            return collection.count_documents({})
        else:
            total_count = 0
            for class_name in classes:
                collection = self.db[class_name]
                total_count += collection.count_documents({})
            return total_count

    def get_augmented(self, obj, field, augment):
        """Join users with their projects based on project IDs"""
        pipeline = [
            {
                "$match": {"_id": ObjectId(obj._id)}
            },
            {
                "$lookup": {
                    "from": f"{augment}",
                    "localField": f"{field}",
                    "foreignField": "_id",
                    "as": f"{obj.__class__.name__}_{field}"
                }
            }
        ]
        augmented_result = list(self.db[obj.__class__.__name__].aggregate(pipeline))
        augmented_objs = []
        for item in augmented_objs:
            restored = classes[obj.__class__.__name__](**str[f"{obj.__class__.name__}_{field}"])
            augmented_objs.append(restored)

        return augmented_objs

    def get_catalog(self, catalog, name):

        collection = self.db[catalog]
        item = collection.find_one({"name": name})
        return item

