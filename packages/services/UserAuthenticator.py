from ..services.DataReader import read_file
from ..services.Hasher import Hasher
from ..services.UserLog import UserLog

import os
from werkzeug.security import check_password_hash
from flask import current_app

from pymongo import MongoClient

class UserAuthenticator:
    def __init__(self, users, username, password):
        self.username = username
        self.password = password
        self.users = users
        self.path = '{users}/{username}'.format(username=username, users=users)

    def auth(self):
        mongo_client = MongoClient(port=27017)
        db = mongo_client.get_database('jdrive')
        collection = db.get_collection(current_app.config['users'])
        user_document = collection.find_one({"username": self.username})

        if user_document != None:
            return check_password_hash(user_document["password"], self.password)
        return False