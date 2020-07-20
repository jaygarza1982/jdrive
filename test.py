import os
import shutil
from RegisterTests import RegisterTests
from LoginTests import LoginTests

users = 'test_users'

#Clean up
if os.path.exists(users):
    shutil.rmtree(users)
os.mkdir(users)

register_tests = RegisterTests(users)
print('Register success', register_tests.test_register_success('test123', '123', '123'))
print('Register mismatch', register_tests.test_register_mismatch('test_user', '123', '1234'))
print('Register duplicate', register_tests.test_register_duplicate('test123', '123', '123'))

login_tests = LoginTests(users)
print('Login success', login_tests.login_success('test123', '123'))