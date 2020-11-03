import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, make_response
)
import os
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.User import User

auth_route = Blueprint('auth_route', __name__)

@auth_route.route('/bp')
def bp_route():
    return 'This did the thing.'

@auth_route.route('/login', methods=['POST'])
def index_login():
    username = request.form['jd-username']
    password = request.form['jd-password']

    user = User(current_app.config['users'], username)

    if user.login(password):
        cookie = '{username} - {rand}'.format(username=username, rand=os.urandom(32))
        resp = make_response(redirect('/home'))
        session[cookie] = username
        resp.set_cookie('login', cookie)
        return resp
    else:
        return 'Invalid username or password.'

@auth_route.route('/register', methods=['POST'])
def index_register():
    username = request.form['jd-username']
    password = request.form['jd-password']
    password_confirm = request.form['jd-password-confirm']

    if password == password_confirm:
        user = User(current_app.config['users'], username)
        if user.register(password):
            return 'Successfully registered as {username}. <a href="/">Return to login here.</a>'.format(username=username)
        return 'Username {username} already exists. <a href="javascript:history.back()">Back to registration.</a>'.format(username=username)
    return 'Passwords do not match. <a href="javascript:history.back()">Back to registration.</a>'