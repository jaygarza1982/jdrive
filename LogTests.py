from app import app

from packages.services.UserLog import UserLog
from FileTests import FileTests

class LogTests:
    def __init__(self, users, admins):
        app.config['users'] = users
        app.config['admins'] = admins
        self.test_app = app.test_client()

    #Test log entries against a list of messages
    def test_log_contents(self, username, messages):
        user_log = UserLog(app.config['users'], username)
        logs = str(user_log.read())

        for message in messages:
            if not message in logs:
                return False

        return True

    #Test to see if a non admin can obtain a log file
    def test_log_not_admin(self, username, password, username_to_read):
        #Login first so we have a cookie
        self.test_app.post('/login', data={'jd-username': username, 'jd-password': password}, follow_redirects=True)

        #Request the log
        download_get = self.test_app.get('admin-view-logs/{user_passed}'.format(user_passed=username_to_read), follow_redirects=True)

        return 'is not an authorized admin. Please add this username to' in str(download_get.data)

    #Test to see if an admin can obtain a log file
    def test_log_with_admin(self, username, password, username_to_read):
        #Login first so we have a cookie
        self.test_app.post('/login', data={'jd-username': username, 'jd-password': password}, follow_redirects=True)

        #Request the log
        download_get = self.test_app.get('admin-view-logs/{user_passed}'.format(user_passed=username_to_read), follow_redirects=True)

        return '{username_to_read} logs'.format(username_to_read=username_to_read) in str(download_get.data) and not 'is not an authorized' in str(download_get.data)

    #Test admin view of user that does not exist
    def test_log_view_no_log(self, username, password, username_to_read):
        #Login first so we have a cookie
        self.test_app.post('/login', data={'jd-username': username, 'jd-password': password}, follow_redirects=True)

        #Request the log
        download_get = self.test_app.get('admin-view-logs/{user_passed}'.format(user_passed=username_to_read), follow_redirects=True)

        return '{username_to_read} logs'.format(username_to_read=username_to_read) in str(download_get.data) and 'No such log file exists' in str(download_get.data)