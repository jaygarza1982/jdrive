from flask import Flask, render_template, make_response, send_from_directory, request, redirect, session, send_file, abort
from werkzeug.utils import secure_filename
from User import User
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ['jdsecret']
app.config['UPLOAD_FOLDER'] = '.'

app.config['users'] = 'users'

def humanize_ts(time, timestamp=False):
    #If we cannot convert the time, skip
    try:
        float(time)
    except:
        return ''

    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    diff = now - datetime.fromtimestamp(float(time))
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(int(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " months ago"
    return str(int(day_diff / 365)) + " years ago"

app.jinja_env.filters['humanize'] = humanize_ts
# app.jinja_environment.filters['humanize'] = humanize_ts

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('public', path)

@app.route('/')
def index_root():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def index_login():
    username = request.form['jd-username']
    password = request.form['jd-password']

    user = User(app.config['users'], username)

    if user.login(password):
        cookie = '{username} - {rand}'.format(username=username, rand=os.urandom(32))
        resp = make_response(redirect('/home'))
        session[cookie] = username
        resp.set_cookie('login', cookie)
        return resp
    else:
        return 'Invalid username or password.'

@app.route('/register', methods=['POST'])
def index_register():
    username = request.form['jd-username']
    password = request.form['jd-password']
    password_confirm = request.form['jd-password-confirm']

    if password == password_confirm:
        user = User(app.config['users'], username)
        if user.register(password):
            return 'Successfully registered as {username}. <a href="/">Return to login here.</a>'.format(username=username)
        return 'Username {username} already exists. <a href="javascript:history.back()">Back to registration.</a>'.format(username=username)
    return 'Passwords do not match. <a href="javascript:history.back()">Back to registration.</a>'

@app.route('/home', defaults={'path': ''})
@app.route('/home/', defaults={'path': ''})
@app.route('/home/<path:path>')
def index_home(path):
    login_cookie = request.cookies['login']
    username = session[login_cookie]
    user = User(app.config['users'], username)

    possible_file = '{users}/{username}/{path}'.format(users=app.config['users'], username=username, path=path)
    # print(possible_file, os.path.isfile(possible_file))
    if os.path.isfile(possible_file):
        return redirect('/file-download/{path}'.format(path=path))
    
    if path == '':
        return render_template('home.html', username=username, files=user.list_files(), dir='root')
    else:
        return render_template('home.html', username=username, files=user.list_files(dir=path), dir=path)

@app.route('/file-upload/<dir>', methods=['POST'])
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

        file.save(os.path.join('{users}/{username}/{dir}'.format(username=username, dir=dir, users=app.config['users']), filename))
    
    return redirect('/home/{dir}'.format(dir=dir))

@app.route('/file-download/<path:path>')
def index_file_download(path):
    login_cookie = request.cookies['login']
    username = session[login_cookie]

    user = User(app.config['users'], username)

    #Send file as attachment
    return user.return_file(path, True)


@app.route('/file-upload-api', methods=['POST'])
def index_file_upload_api():
    username = request.form['username']
    password = request.form['password']

    user = User(app.config['users'], username)
    if user.login(password):
        file = request.files.getlist('jd-files')[0]
        filename = file.filename
        file.save(os.path.join('{users}/{username}'.format(username=username, users=app.config['users']), filename))
    else:
        return 'Invalid username or password.'

    return 'Success!'

@app.route('/file-delete-api', methods=['POST'])
def index_file_delete_api():
    username = request.form['username']
    password = request.form['password']

    user = User(app.config['users'], username)
    if user.login(password):
        filename = request.form['file-to-delete']
        path = '{users}/{username}/{filename}'.format(username=username, filename=filename, users=app.config['users'])
        if os.path.exists(path):
            os.remove(path)
    else:
        return 'Invalid username or password.'

    return 'Success!'

@app.route('/file-rename-api', methods=['POST'])
def index_file_rename_api():
    username = request.form['username']
    password = request.form['password']

    user = User(app.config['users'], username)
    if user.login(password):
        old_filename = request.form['file-to-rename']
        new_filename = request.form['file-new-name']

        old_path = '{users}/{username}/{filename}'.format(username=username, filename=old_filename, users=app.config['users'])
        new_path = '{users}/{username}/{filename}'.format(username=username, filename=new_filename, users=app.config['users'])
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
    else:
        abort(403)

    return 'Success!'

@app.route('/file-stats-api/<path>', methods=['POST'])
def index_file_status_api(path):
    username = request.form['username']
    password = request.form['password']

    user = User(app.config['users'], username)
    if user.login(password):
        stats = user.list_files(dir=path)
        stats_string = ''
        
        for stat in stats:
            stats_string += '{name},{date}\n'.format(name=stat['name'], date=stat['last_modified'])
            # print(stats_string)
        
        return stats_string
    else:
        abort(403)

@app.route('/file-download-api/<file>', methods=['POST'])
def index_file_download_api(file):
    username = request.form['username']
    password = request.form['password']

    user = User(app.config['users'], username)
    if user.login(password):
        if not os.path.isdir('{users}/{username}/{file}'.format(username=username, file=file, users=app.config['users'])):
            path = os.path.join('{users}/{username}'.format(username=username, users=app.config['users']), file)

            return send_file(path)
        return '{file} is a directory'.format(file=file)
    abort(403)

if __name__ == '__main__':
    #Create the users directory if it does not exist
    if not os.path.exists(app.config['users']):
        os.mkdir(app.config['users'])
        
    app.run('0.0.0.0', port=3005)