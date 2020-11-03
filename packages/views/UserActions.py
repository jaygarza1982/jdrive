import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, make_response
)
import os
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.User import User

user_action_route = Blueprint('user_action_route', __name__)

@user_action_route.route('/home', defaults={'path': ''})
@user_action_route.route('/home/', defaults={'path': ''})
@user_action_route.route('/home/<path:path>')
def index_home(path):
    login_cookie = request.cookies['login']
    username = session[login_cookie]
    user = User(current_app.config['users'], username)

    possible_file = '{users}/{username}/{path}'.format(users=current_app.config['users'], username=username, path=path)
    # print(possible_file, os.path.isfile(possible_file))
    if os.path.isfile(possible_file):
        return redirect('/file-download/{path}'.format(path=path))
    
    if path == '':
        return render_template('home.html', username=username, files=user.list_files(), dir='root')
    else:
        return render_template('home.html', username=username, files=user.list_files(dir=path), dir=path)

@user_action_route.route('/file-upload/<dir>', methods=['POST'])
def index_file_upload(dir):
    # print(request.files.getlist('jd-files'))
    login_cookie = request.cookies['login']
    username = session[login_cookie]

    # print(dir)
    for file in request.files.getlist('jd-files'):
        # TODO: Add secure filename with spaces and other characters allowed
        filename = (file.filename)

        if dir == 'root':
            dir = ''

        file.save(os.path.join('{users}/{username}/{dir}'.format(username=username, dir=dir, users=current_app.config['users']), filename))
    
    return redirect('/home/{dir}'.format(dir=dir))

@user_action_route.route('/file-download/<path:path>')
def index_file_download(path):
    login_cookie = request.cookies['login']
    username = session[login_cookie]

    user = User(current_app.config['users'], username)

    #Send file as attachment
    return user.return_file(path, True)