from User import User
from UserLog import UserLog

class Admin(User):
    def __init__(self, admins, username):
        self.username = username
        self.admins = admins
    
    def _auth(self):
        #Check if is admin in admins file
        with open(self.admins, 'r') as admin_file:
            return self.username in admin_file.readlines()

    def read_log(self, user):
        user_log = UserLog(user.users, user.username)
        if self._auth():
            return user_log.read()
        message = '{username} is not an authorized admin. Please add this username to {admins}'.format(username=self.username, admins=self.admins)
        return user_log.read_error(message)