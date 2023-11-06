from flask import Blueprint, request, current_app
from werkzeug.security import generate_password_hash
from geektrac.db import get_db_handler, check_if_user_exists, check_user_passwd, insert_user_to_db

from geektrac.util import token_required
from datetime import date,datetime, timedelta

import jwt

dbhandle = get_db_handler()

user_creation = Blueprint('user_creation', __name__, url_prefix = '/user')

@user_creation.route('/create', methods = ['GET'])
def user_creation_form():
    return ""

@user_creation.route('/create', methods = ['POST'])
def create_user():
    user_form = request.form
    params_required = ['username', 'password']

    for param in params_required:
        if param in user_form:
            continue
        return f'{param} not found', 400

    username = user_form['username']
    password = user_form['password']

    print(username, password)

    if check_if_user_exists(username):
        return "username taken", 409

    status = insert_user_to_db(username, password)
    if not status:
        return "Server error", 500
    
    
    return "User success fully created", 200


@user_creation.route('/login', methods = ['POST'])
def user_login():
    user_form = request.form
    params_required = ['username', 'password']

    for param in params_required:
        if param in user_form:
            continue
        return f'{param} not found', 400

    username = user_form['username']
    password = user_form['password']

    if not check_user_passwd(username, password):
        return "invalid user details", 403
    
    return generate_jwt(username)

def generate_jwt(username):
    jwt_token = jwt.encode({
        'username': username,
        'valid_till': str(datetime.utcnow() + timedelta(minutes = 3000))
    }, current_app.config['SECRET_KEY'], "HS256")

    return jwt_token

@user_creation.route('/login', methods = ['GET'])
def user_login_form():
    return ""


user_detail = Blueprint('user_detail', __name__, url_prefix = '/')

@user_detail.route('/ping', methods = ['GET'])
@token_required
def ping(token_data):
    return {
        "user": token_data['username']
    }, 200

@user_detail.route('/leetcode', methods = ['GET'])
@token_required
def leetcode_stats(token_data):
    return {
        
    }