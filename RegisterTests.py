from run import app

class RegisterTests:
    def __init__(self, users):
        app.config['users'] = users
        self.test_app = app.test_client()
    
    def test_register_success(self, username, password, password_confirm):
        reg = self.test_app.post('/register', data={'jd-username': username, 'jd-password': password, 'jd-password-confirm': password_confirm})

        success_message = 'Successfully registered as {username}'.format(username=username)
        return success_message in str(reg.data)
    
    def test_register_mismatch(self, username, password, password_confirm):
        reg = self.test_app.post('/register', data={'jd-username': username, 'jd-password': password, 'jd-password-confirm': password_confirm})

        success_message = 'Passwords do not match.'
        return success_message in str(reg.data)

    def test_register_duplicate(self, username, password, password_confirm):
        reg = self.test_app.post('/register', data={'jd-username': username, 'jd-password': password, 'jd-password-confirm': password_confirm})

        success_message = 'Username {username} already exists'.format(username=username)
        return success_message in str(reg.data)


# user = User('users', 'test')
# user.register('123')
# print(user.login('123'))
# print(user.login('32'))

