import os
import shutil

from RegisterTests import RegisterTests
from LoginTests import LoginTests
from FileTests import FileTests

users = 'test_users'

#Clean up
if os.path.exists(users):
    shutil.rmtree(users)
os.mkdir(users)

register_tests = RegisterTests(users)
print(register_tests.test_register_success('test123', '123', '123'), 'Register success')
print(register_tests.test_register_mismatch('test_user', '123', '1234'), 'Register mismatch')
print(register_tests.test_register_duplicate('test123', '123', '123'), 'Register duplicate')

login_tests = LoginTests(users)
print(login_tests.login_success('test123', '123'), 'Login success')
print(login_tests.login_invalid_credentials('test321', '123'), 'Login invalid username')
print(login_tests.login_invalid_credentials('test123', '124'), 'Login invalid credentials')

file_tests = FileTests(users)
print(file_tests.file_upload_success('test123', '123', 'test1.txt'), 'Uploading test1.txt')
print(file_tests.multiple_file_upload_success('test123', '123', ['jdrive.png', 'utah.jpg']), 'Uploading multiple files: jdrive.png, utah.jpg')
print(file_tests.file_download_success('test123', '123', 'jdrive.png'), 'File download test jdrive.png')