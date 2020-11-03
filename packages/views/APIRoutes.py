import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, make_response, abort, send_file
)
import os
from ..models.User import User

api_route = Blueprint('api_route', __name__)

@api_route.route('/file-upload-api', methods=['POST'])
def index_file_upload_api():
    username = request.form['username']
    password = request.form['password']

    user = User(current_app.config['users'], username)
    if user.login(password):
        file = request.files.getlist('jd-files')[0]
        filename = file.filename
        user_dir = '{users}/{username}'.format(username=username, users=current_app.config['users'])
        path_to_save = os.path.join(user_dir, filename)

        #Do not override a directory when uploading
        if not os.path.isdir(path_to_save):
            file.save(path_to_save)
    else:
        return 'Invalid username or password.'

    return 'Success!'

@api_route.route('/file-delete-api', methods=['POST'])
def index_file_delete_api():
    username = request.form['username']
    password = request.form['password']

    user = User(current_app.config['users'], username)
    if user.login(password):
        filename = request.form['file-to-delete']
        path = '{users}/{username}/{filename}'.format(username=username, filename=filename, users=current_app.config['users'])
        if os.path.exists(path):
            os.remove(path)
    else:
        return 'Invalid username or password.'

    return 'Success!'

@api_route.route('/file-rename-api', methods=['POST'])
def index_file_rename_api():
    username = request.form['username']
    password = request.form['password']

    user = User(current_app.config['users'], username)
    if user.login(password):
        old_filename = request.form['file-to-rename']
        new_filename = request.form['file-new-name']

        old_path = '{users}/{username}/{filename}'.format(username=username, filename=old_filename, users=current_app.config['users'])
        new_path = '{users}/{username}/{filename}'.format(username=username, filename=new_filename, users=current_app.config['users'])
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
    else:
        abort(403)

    return 'Success!'

@api_route.route('/file-stats-api/<path>', methods=['POST'])
def index_file_status_api(path):
    username = request.form['username']
    password = request.form['password']

    user = User(current_app.config['users'], username)
    if user.login(password):
        stats = user.list_files(dir=path)
        stats_string = ''
        
        for stat in stats:
            stats_string += '{name},{date}\n'.format(name=stat['name'], date=stat['last_modified'])
            # print(stats_string)
        
        return stats_string
    else:
        abort(403)

@api_route.route('/file-download-api/<file>', methods=['POST'])
def index_file_download_api(file):
    username = request.form['username']
    password = request.form['password']

    user = User(current_app.config['users'], username)
    if user.login(password):
        if not os.path.isdir('{users}/{username}/{file}'.format(username=username, file=file, users=current_app.config['users'])):
            path = os.path.join('{users}/{username}'.format(username=username, users=current_app.config['users']), file)

            return send_file(path)
        return '{file} is a directory'.format(file=file)
    abort(403)