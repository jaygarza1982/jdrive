import os
import shutil

from RegisterTests import RegisterTests
from LoginTests import LoginTests
from FileTests import FileTests
from LogTests import LogTests

users = 'test_users'
admins = '.test_admins'

#Clean up
if os.path.exists(users):
    shutil.rmtree(users)
os.mkdir(users)

#Registration tests
register_tests = RegisterTests(users)
print(register_tests.test_register_success('test123', '123', '123'), 'Register success')
print(register_tests.test_register_mismatch('test_user', '123', '1234'), 'Register mismatch')
print(register_tests.test_register_duplicate('test123', '123', '123'), 'Register duplicate')

#Directory and file creation for nested tests
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

#Login tests
login_tests = LoginTests(users)
print(login_tests.login_success('test123', '123'), 'Login success')
print(login_tests.login_invalid_credentials('test321', '123'), 'Login invalid username')
print(login_tests.login_invalid_credentials('test123', '124'), 'Login invalid credentials')

#File upload and download tests
file_tests = FileTests(users)
print(file_tests.file_upload_success('test123', '123', 'test1.txt'), 'Uploading test1.txt')
print(file_tests.multiple_file_upload_success('test123', '123', ['jdrive.png', 'utah.jpg']), 'Uploading multiple files: jdrive.png, utah.jpg')
print(file_tests.file_upload_api_invalid_credentials('test123', '233', 'test-api-fail-upload.txt'), 'File upload API success')
print(file_tests.file_upload_api_success('test123', '123', 'test-api-upload.txt'), 'File upload API invalid credentials')
print(file_tests.file_download_success('test123', '123', 'jdrive.png'), 'File download test jdrive.png')
print(file_tests.file_download_fail_secret('test123', '123', 'passwd - ', 'Requesting a secret file "passwd -'), 'File download test passwd - ')
print(file_tests.file_download_fail_secret('test123', '123', 'salt - ', 'Requesting a secret file "salt -'), 'File download test salt - ')
print(file_tests.file_download_fail_secret('test123', '123', 'log - ', 'Requesting a secret file "log -'), 'File download test log - ')
print(file_tests.file_download_success('test123', '123', 'testing dir/testing file.txt'), 'File in directory')
print(file_tests.file_download_success('test123', '123', 'testing dir/folder in testing dir/testing file in testing dir.txt'), 'File in nested directory')
print(file_tests.file_download_api_success('test123', '123', 'jdrive.png'), 'File API download jdrive.png')
print(file_tests.file_download_api_success('test123', '123', 'utah.jpg'), 'File API download utah.jpg')
print(file_tests.file_download_api_bad_credentials('test123', '1233', 'utah.jpg'), 'File API bad credentials utah.jpg')

#Create test admins file, register the admin
with open(admins, 'w') as admins_file:
    admins_file.write('theman')
print(register_tests.test_register_success('theman', 'themanpass', 'themanpass'), 'Registering admin test')

#Logging tests
log_tests = LogTests(users, admins)
log_tests.test_log_contents('test123', ['User registered', 'Returning test_users/test123/jdrive.png', 'Failed credentials'])
print(log_tests.test_log_not_admin('test123', '123', 'test123'), 'Non admin log view test')
print(log_tests.test_log_not_admin('test123', '123', 'testnoexist123'), 'Non admin log view test of invalid username')
print(log_tests.test_log_with_admin('theman', 'themanpass', 'test123'), 'Admin log view test')
print(log_tests.test_log_view_no_log('theman', 'themanpass', 'testnoexists'), 'Admin log view of invalid username')