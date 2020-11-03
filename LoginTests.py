from app import app

class LoginTests:
    def __init__(self, users):
        app.config['users'] = users
        self.test_app = app.test_client()

    def login_success(self, username, password):
        login = self.test_app.post('/login', data={'jd-username': username, 'jd-password': password}, follow_redirects=True)

        login_success_message = 'JD Rive - <a href="/home">{username}</a>'.format(username=username)

        return login_success_message in str(login.data)

    def login_invalid_credentials(self, username, password):
        login = self.test_app.post('/login', data={'jd-username': username, 'jd-password': password}, follow_redirects=True)

        login_success_message = 'Invalid username or password.'
        
        return login_success_message in str(login.data)