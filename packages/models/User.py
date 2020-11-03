import os, hashlib, time
import datetime

from flask import send_file

from ..services.UserLog import UserLog
from ..services.Hasher import Hasher
from ..services.UserAuthenticator import UserAuthenticator
from ..services.UserRegisterer import UserRegisterer

class User:
    def __init__(self, users, username):
        self.username = username
        self.users = users
        self.path = '{users}/{username}'.format(username=username, users=users)
        self.user_log = UserLog(users, username)
        self.secret_files = ['passwd - ', 'salt - ', 'log - ']

    def login(self, passwd):
        userAuth = UserAuthenticator(self.users, self.username, passwd)

        return userAuth.auth()

    def register(self, passwd):
        user_register = UserRegisterer(self.users, self.username, passwd)

        return user_register.register()

    def write_file(self, filename, file_id, content):
        with open('{path}/{filename} - {file_id}'.format(filename=filename, file_id=file_id, username=self.username, path=self.path), 'wb') as file:
            file.write(content)

    def return_file(self, path, attachment):
        file_to_send = os.path.join('{users}/{username}'.format(username=self.username, users=self.users), path)

        #Check to make sure we are not sending a directory
        if os.path.isdir(file_to_send):
            return 'You are trying to download a directory.'

        #Before sending a file, check the file name to see if we are sending a secret file
        filename = str(path).split('/')[-1]

        for secret_file in self.secret_files:
            if filename == secret_file:
                return 'Requesting a secret file "{filename}". This is not allowed.'.format(filename=filename)
        
        self.user_log.return_file(file_to_send)
        return send_file(file_to_send, as_attachment=attachment)

    def list_files(self, dir=''):
        if dir == 'root':
            dir = ''

        files = os.listdir('{root}/{dir}'.format(root=self.path, dir=dir))

        # Remove passwd and hash
        for secret_file in self.secret_files:
            if secret_file in files:
                files.remove(secret_file)

        file_listings = []

        for file in files:
            file_listings.append(dict())
            file_listings[-1]['name'] = file

            if dir == '':
                file_path = '{path}/{file}'.format(username=self.username, file=file, path=self.path)
            else:
                file_path = '{path}/{dir}/{file}'.format(username=self.username, file=file, dir=dir, path=self.path)
            
            file_listings[-1]['crc'] = ''
            file_listings[-1]['last_modified'] = ''
            if not os.path.isdir(file_path):
                sum256 = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()
                file_listings[-1]['crc'] = sum256
                
                file_listings[-1]['last_modified'] = (os.stat(file_path).st_mtime) #time.ctime(os.stat(file_path).st_mtime)
                # print(file, file_listings[-1]['last_modified'])

        return file_listings