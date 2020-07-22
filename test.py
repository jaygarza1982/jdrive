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

testing_dir = '{users}/test123/testing dir'.format(users=users)
if os.path.exists(testing_dir):
    shutil.rmtree(testing_dir)
os.mkdir(testing_dir)
testing_file = open('{testing_dir}/testing file.txt'.format(testing_dir=testing_dir), 'w')
testing_file.write('This is some content within testing file.txt')
testing_file.close()

testing_dir = '{users}/test123/testing dir/folder in testing dir'.format(users=users)
if os.path.exists(testing_dir):
    shutil.rmtree(testing_dir)
os.mkdir(testing_dir)
testing_file = open('{testing_dir}/testing file in testing dir.txt'.format(testing_dir=testing_dir), 'w')
testing_file.write('This is some content within a testing file that is in another directory!')
testing_file.close()

login_tests = LoginTests(users)
print(login_tests.login_success('test123', '123'), 'Login success')
print(login_tests.login_invalid_credentials('test321', '123'), 'Login invalid username')
print(login_tests.login_invalid_credentials('test123', '124'), 'Login invalid credentials')

file_tests = FileTests(users)
print(file_tests.file_upload_success('test123', '123', 'test1.txt'), 'Uploading test1.txt')
print(file_tests.multiple_file_upload_success('test123', '123', ['jdrive.png', 'utah.jpg']), 'Uploading multiple files: jdrive.png, utah.jpg')
print(file_tests.file_download_success('test123', '123', 'jdrive.png'), 'File download test jdrive.png')
print(file_tests.file_download_fail_secret('test123', '123', 'passwd - ', 'Requesting a secret file "passwd -'), 'File download test passwd - ')
print(file_tests.file_download_fail_secret('test123', '123', 'salt - ', 'Requesting a secret file "salt -'), 'File download test salt - ')
print(file_tests.file_download_success('test123', '123', 'testing dir/testing file.txt'), 'File in directory')
print(file_tests.file_download_success('test123', '123', 'testing dir/folder in testing dir/testing file in testing dir.txt'), 'File in nested directory')
print(file_tests.file_download_api_success('test123', '123', 'jdrive.png'), 'File API download jdrive.png')
print(file_tests.file_download_api_success('test123', '123', 'utah.jpg'), 'File API download utah.jpg')
print(file_tests.file_download_api_bad_credentials('test123', '1233', 'utah.jpg'), 'File API bad credentials utah.jpg')