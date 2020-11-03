from pymongo import MongoClient
from datetime import datetime
from flask import current_app

class UserLogReader:

    def __init__(self, username, users):
        self.username = username
        self.users = users
    
    def read(self):
        current_time = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

        mongo_client = MongoClient(port=27017)
        db = mongo_client.get_database('jdrive')
        collection = db.get_collection(self.users)
        user_query = collection.find_one({'username': self.username})
        if user_query != None:
            return user_query["log"]
        return [{'date': '0', 'time': '0', 'message': 'No such log file exists.'}]
