
def read_file(username, path, filename):
    file_path = '{path}/{filename}'.format(username=username, filename=filename, path=path)
    return open(file_path, 'rb').read()
