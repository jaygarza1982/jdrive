from packages.models.User import User
from packages.services.UserLog import UserLog
from packages.services.AdminReader import AdminReader

class Admin(User):
    def __init__(self, admins, username):
        self.username = username
        self.admins = admins
    
    def _auth(self):
        reader = AdminReader(self.admins)
        return self.username in reader.get_admins()

    def read_log(self, user):
        user_log = UserLog(user.users, user.username)
        if self._auth():
            return user_log.read()
        message = '{username} is not an authorized admin. Please add this username to {admins}'.format(username=self.username, admins=self.admins)
        return user_log.read_error(message)