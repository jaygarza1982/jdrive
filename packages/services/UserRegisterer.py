from ..services.DataReader import read_file
from ..services.Hasher import Hasher
from ..services.UserLog import UserLog
from ..models.UserModel import UserModel

from flask import current_app

import os
from pymongo import MongoClient

class UserRegisterer:
    def __init__(self, users, username, password):
        self.username = username
        self.password = password
        self.users = users
        self.path = '{users}/{username}'.format(username=self.username, users=users)

    def register(self):
        mongo_client = MongoClient(port=27017)
        
        db = mongo_client.get_database('jdrive')
        collection_name = current_app.config['users']
        collection = db.get_collection(collection_name)
        user_query = collection.find_one({'username': self.username})

        if user_query == None:
            # We insert
            user_model = UserModel(self.username, self.password)
            collection.insert_one(user_model.get())
            os.mkdir(self.path)

            return True
        else:
            return False