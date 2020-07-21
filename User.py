import os, hashlib, time
import datetime

class User:
    

    def __init__(self, users, username):
        self.username = username
        self.users = users
        self.path = '{users}/{username}'.format(username=username, users=self.users)
        self.secret_files = ['passwd - ', 'salt - ']

    def login(self, passwd):
        if os.path.exists(self.path):
            hash = self.read_file('passwd - ')
            salt = self.read_file('salt - ')

            return self.get_hash(passwd, salt) == hash
        else:
            return False

    def register(self, passwd):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            hash_salt = self.get_hash_and_salt(passwd)
            hash = hash_salt[0]
            salt = hash_salt[1]

            self.write_file('passwd', '', hash)
            self.write_file('salt', '', salt)

            print('Registering {username}.'.format(username=self.username))
            return True
        return False

    def write_file(self, filename, file_id, content):
        with open('{path}/{filename} - {file_id}'.format(filename=filename, file_id=file_id, username=self.username, path=self.path), 'wb') as file:
            file.write(content)

    def read_file(self, filename):
        file_path = '{path}/{filename}'.format(username=self.username, filename=filename, path=self.path)
        return open(file_path, 'rb').read()

    def list_files(self, dir=''):
        if dir == 'root':
            dir = ''

        files = os.listdir('{root}/{dir}'.format(root=self.path, dir=dir))

        # Remove passwd and hash
        for secret_file in self.secret_files:
            if secret_file in files:
                files.remove(secret_file)

        file_listings = []

        for file in files:
            file_listings.append(dict())
            file_listings[-1]['name'] = file

            if dir == '':
                file_path = '{path}/{file}'.format(username=self.username, file=file, path=self.path)
            else:
                file_path = '{path}/{dir}/{file}'.format(username=self.username, file=file, dir=dir, path=self.path)
            
            file_listings[-1]['crc'] = ''
            file_listings[-1]['last_modified'] = ''
            if not os.path.isdir(file_path):
                sum256 = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()
                file_listings[-1]['crc'] = sum256
                
                file_listings[-1]['last_modified'] = (os.stat(file_path).st_mtime) #time.ctime(os.stat(file_path).st_mtime)
                # print(file, file_listings[-1]['last_modified'])

        return file_listings

    # Get a hash and a salt
    def get_hash_and_salt(self, password):
        salt = os.urandom(128)  # Remember this

        key = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000,  # It is recommended to use at least 100,000 iterations of SHA-256
            dklen=128  # Get a 128 byte key
        )

        return (key, salt,)

    # Get a hash with a salt
    def get_hash(self, password, salt):
        hash = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000,  # It is recommended to use at least 100,000 iterations of SHA-256
            dklen=128  # Get a 128 byte key
        )

        return hash