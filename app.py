from flask import Flask, render_template, make_response, send_from_directory, request, redirect, session, send_file, abort
from werkzeug.utils import secure_filename
# from User import User
from packages.models.User import User
from packages.models.Admin import Admin
import os

from packages.services.Humanizer import humanize_ts

from packages.views.auth import auth_route
from packages.views.UserActions import user_action_route
from packages.views.APIRoutes import api_route

# Set up configuration
app = Flask(__name__)
app.secret_key = os.environ['jdsecret']
app.config['UPLOAD_FOLDER'] = '.'
app.config['users'] = 'users'
app.config['admins'] = '.admins'

app.jinja_env.filters['humanize'] = humanize_ts

# Register blueprints and routes
app.register_blueprint(auth_route)
app.register_blueprint(user_action_route)
app.register_blueprint(api_route)

#If admins file does not exist, create it
if not os.path.exists(app.config['admins']):
    open(app.config['admins'], 'w').close()

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('public', path)

@app.route('/')
def index_root():
    return render_template('index.html')

#----- Admin paths -----

@app.route('/admin-view-logs/<user_passed>')
def index_admin_view_logs(user_passed):
    login_cookie = request.cookies['login']
    username = session[login_cookie]
    admin = Admin(app.config['admins'], username)

    user_to_read = User(app.config['users'], user_passed)
    return render_template('user-log.html', username=user_passed, logs=admin.read_log(user_to_read))

if __name__ == '__main__':
    #Create the users directory if it does not exist
    if not os.path.exists(app.config['users']):
        os.mkdir(app.config['users'])
        
    app.run('0.0.0.0', port=3005)