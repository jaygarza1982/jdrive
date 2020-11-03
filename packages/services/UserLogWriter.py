from pymongo import MongoClient
from datetime import datetime
from flask import current_app

class UserLogWriter:

    def __init__(self, username):
        self.username = username
        # self.log_file = '{users}/{username}/log - '.format(users=self.users, username=self.username)
    
    def write(self, message):
        current_time = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

        to_write = '{time} - {message}'.format(time=current_time, message=message)
        mongo_client = MongoClient(port=27017)
        db = mongo_client.get_database('jdrive')
        collection = db.get_collection(current_app.config['users'])
        collection.update({'username': self.username}, {'$push': {
            'log':
            {
                'date': current_time.split(' ')[0],
                'time': current_time.split(' ')[1],
                'message': message,
            }
        }})