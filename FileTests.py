from run import app
import os

class FileTests:
    def __init__(self, users):
        app.config['users'] = users
        self.test_app = app.test_client()

    def file_upload_success(self, username, password, filename):
        #Login first so we have a cookie
        login = self.test_app.post('/login', data={'jd-username': username, 'jd-password': password}, follow_redirects=True)

        files = []
        files.append((open('test_files/{filename}'.format(filename=filename), 'rb'), filename,))
        
        data = {
            'jd-files': files,
        }
        
        upload_post = self.test_app.post('/file-upload/root'.format(filename=filename), content_type='multipart/form-data', data=data, follow_redirects=True)
        # print(upload_post.data)
        return os.path.isfile('{users}/{username}/{filename}'.format(users=app.config['users'], username=username, filename=filename))