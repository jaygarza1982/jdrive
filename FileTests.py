from run import app
import os, hashlib

class FileTests:
    def __init__(self, users):
        app.config['users'] = users
        self.test_app = app.test_client()

    def file_upload_success(self, username, password, filename):
        #Login first so we have a cookie
        self.test_app.post('/login', data={'jd-username': username, 'jd-password': password}, follow_redirects=True)

        files = []
        files.append((open('test_files/{filename}'.format(filename=filename), 'rb'), filename,))
        
        data = {
            'jd-files': files,
        }
        
        self.test_app.post('/file-upload/root'.format(filename=filename), content_type='multipart/form-data', data=data, follow_redirects=True)
        # print(upload_post.data)
        return os.path.isfile('{users}/{username}/{filename}'.format(users=app.config['users'], username=username, filename=filename))

    def file_upload_api_success(self, username, password, filename):
        files = []
        files.append((open('test_files/{filename}'.format(filename=filename), 'rb'), filename,))
        
        #Add username and password to API for authentication
        data = {
            'username': username,
            'password': password,
            'jd-files': files,
        }

        self.test_app.post('/file-upload-api', data=data)

        return os.path.isfile('{users}/{username}/{filename}'.format(users=app.config['users'], username=username, filename=filename))

    def file_upload_api_invalid_credentials(self, username, password, filename):
        return not self.file_upload_api_success(username, password, filename)

    def multiple_file_upload_success(self, username, password, filenames):
        #Login first so we have a cookie
        self.test_app.post('/login', data={'jd-username': username, 'jd-password': password}, follow_redirects=True)

        #Append open and filename as a tuple into files
        files = []
        for filename in filenames:
            files.append((open('test_files/{filename}'.format(filename=filename), 'rb'), filename,))

        #Set the data for our post request
        data = {
            'jd-files': files,
        }

        #Send a post request uploading multiple files
        self.test_app.post('/file-upload/root'.format(filename=filename), content_type='multipart/form-data', data=data, follow_redirects=True)
        
        #List files from test_files directory, check that each uploaded file made it into the directory of user
        #If a name is not found, the upload has failed
        listing = os.listdir('test_files')
        for filename in filenames:
            if not filename in listing:
                return False

        return True

    def file_download_success(self, username, password, filename):
        #Login first so we have a cookie
        self.test_app.post('/login', data={'jd-username': username, 'jd-password': password}, follow_redirects=True)

        #Request the file
        download_get = self.test_app.get('/home/{filename}'.format(filename=filename), follow_redirects=True)

        #Calculate the SHA256 of both the file in the test_files dir and from the get request
        sha_downloaded = hashlib.sha256(download_get.data).hexdigest()
        sha_test_file = hashlib.sha256(open('test_files/{filename}'.format(filename=filename), 'rb').read()).hexdigest()

        #Return if they are both equal
        return sha_downloaded == sha_test_file

    def file_download_fail_secret(self, username, password, filename, message):
        #Login first so we have a cookie
        self.test_app.post('/login', data={'jd-username': username, 'jd-password': password}, follow_redirects=True)

        #Request the file
        download_get = self.test_app.get('/home/{filename}'.format(filename=filename), follow_redirects=True)

        return message in str(download_get.data)

    def file_download_api_success(self, username, password, filename):
        data = {
            'username': username,
            'password': password,
        }

        #Request the file
        download_post = self.test_app.post('/file-download-api/{filename}'.format(filename=filename), data=data, follow_redirects=True)

        #Calculate the SHA256 of both the file in the test_files dir and from the get request
        sha_downloaded = hashlib.sha256(download_post.data).hexdigest()
        sha_test_file = hashlib.sha256(open('test_files/{filename}'.format(filename=filename), 'rb').read()).hexdigest()

        #Return if they are both equal
        return sha_downloaded == sha_test_file

    def file_download_api_bad_credentials(self, username, password, filename):
        data = {
            'username': username,
            'password': password,
        }

        #Request the file
        download_post = self.test_app.post('/file-download-api/{filename}'.format(filename=filename), data=data, follow_redirects=True)

        #Calculate the SHA256 of both the file in the test_files dir and from the post request
        sha_downloaded = hashlib.sha256(download_post.data).hexdigest()
        sha_test_file = hashlib.sha256(open('test_files/{filename}'.format(filename=filename), 'rb').read()).hexdigest()

        #If we supply bad credentials, we want access denied
        return download_post.status_code == 403 and sha_downloaded != sha_test_file