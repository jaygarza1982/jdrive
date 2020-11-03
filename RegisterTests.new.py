import unittest
from app import app

class RegisterTests(unittest.TestCase):
    def __init__(self, users):
        app.config['users'] = users
        self.test_app = app.test_client()
    
    def test_register_success(self, username, password, password_confirm):
        reg = self.test_app.post('/register', data={'jd-username': username, 'jd-password': password, 'jd-password-confirm': password_confirm})

        success_message = 'Successfully registered as {username}'.format(username=username)
        print(reg.data)
        
        self.assertTrue(success_message in str(reg.data))
        # return success_message in str(reg.data)
    
    def test_register_mismatch(self, username, password, password_confirm):
        reg = self.test_app.post('/register', data={'jd-username': username, 'jd-password': password, 'jd-password-confirm': password_confirm})

        success_message = 'Passwords do not match.'
        self.assertTrue(success_message in str(reg.data))
        # return success_message in str(reg.data)

    def test_register_duplicate(self, username, password, password_confirm):
        reg = self.test_app.post('/register', data={'jd-username': username, 'jd-password': password, 'jd-password-confirm': password_confirm})

        success_message = 'Username {username} already exists'.format(username=username)
        self.assertTrue(success_message in str(reg.data))
        # return success_message in str(reg.data)

if __name__ == '__main__':
    unittest.main()