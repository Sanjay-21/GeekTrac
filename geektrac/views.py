from flask import Blueprint, request, current_app, make_response, render_template
from werkzeug.security import generate_password_hash
from geektrac.db import get_db_handler, check_if_user_exists, check_user_passwd, insert_user_to_db, add_platform_uname_to_db

from geektrac.util import token_required, leetcode_handle, codechef_handle, get_codechef_handle, get_leetcode_handle
from datetime import date,datetime, timedelta

import jwt

dbhandle = get_db_handler()

user_creation = Blueprint('user_creation', __name__, url_prefix = '/user')
user_detail = Blueprint('user_detail', __name__, url_prefix = '/')


@user_creation.route('/create', methods = ['GET'])
def user_creation_form():
    return ""

@user_creation.route('/create', methods = ['POST'])
def create_user():
    user_form = request.form
    params_required = ['username', 'password', 'email']

    for param in params_required:
        if param in user_form:
            continue
        return f'{param} not found', 400

    username = user_form['username']
    password = user_form['password']
    email = user_form['email']

    print(username, password)

    if check_if_user_exists(username):
        return "username taken", 409

    status = insert_user_to_db(username, password, email)
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
    
    jwtToken = generate_jwt(username)
    resp = make_response()  
    resp.set_cookie('Authorization', jwtToken, secure=True, httponly=True) 

    return resp

def generate_jwt(username):
    jwt_token = jwt.encode({
        'username': username,
        'valid_till': str(datetime.utcnow() + timedelta(minutes = 3000))
    }, current_app.config['SECRET_KEY'], "HS256")

    return jwt_token

@user_creation.route('/login', methods = ['GET'])
def user_login_form():
    return render_template('basic_login.html')

@user_creation.route('/logout', methods = ['GET'])
@token_required
def logout(token_data):
    resp = make_response()
    resp.set_cookie('Authorization', '', secure=True, httponly=True)

    return resp

@user_detail.route('/ping', methods = ['GET'])
@token_required
def ping(token_data):
    return {
        "user": token_data['username']
    }, 200

@user_detail.route('/leetcode', methods = ['GET'])
@token_required
def leetcode_stats(token_data):
    return view_stat(token_data['username'], 'leetcode')

@user_detail.route('/codechef', methods = ['GET'])
@token_required
def codechef_stats(token_data):
    return view_stat(token_data['username'], 'codechef')

def view_stat(username, platform):
    if not dbhandle:
        get_db_handler()
    
    if platform == 'leetcode':
        stats = list(dbhandle.view('userdetails/leetcode_stat', key = username))
        if len(stats) <= 0:
            return {}
        return stats[0]['value']
        
    elif platform == 'codechef':
        stats = list(dbhandle.view('userdetails/codechef_stat', key = username))
        if len(stats) <= 0:
            return {}
        return stats[0]

    return {}


@user_detail.route('/platform')
@token_required
def add_platform_uname(token_data):
    user_form = request.form
    params_required = ['platform', 'username']

    for param in params_required:
        if param in user_form:
            continue
        return f'{param} not found', 400

    platform = user_form['platform']
    username = user_form['username']

    add_platform_uname_to_db(token_data['username'], platform, username)

    return "username added", 200


@user_detail.route('/update', methods = ['POST'])
@token_required
def update_platforms(token_data):
    username = token_data['username']

    user = list(dbhandle.view('userdetails/platform_uname', key=username))
    if len(user) <= 0:
        return "add username for platforms", 200
    
    user = user[0]['value']

    # if 'platform_uname' not in user:
    #     return "add username for platforms", 200
    
    for platform, uname in user.items():
        scrap_platform(platform, username)
    
    return "Successfully scrapped", 200


def scrap_platform(platform, uname):
#     platforms = {
#         'codechef': (codechef_handle, get_codechef_handle),
#         'leetcode': (leetcode_handle, get_leetcode_handle),
#     }

#     if platform not in platforms:
#         return ""
    
#     handle = platforms[platform]
#     if handle[0] is None:
#         handle[1]()
    
#     [0].scrap_now(username)

    global leetcode_handle, codechef_handle
    
    if platform == 'leetcode':
        if leetcode_handle is None:
            leetcode_handle = get_leetcode_handle()
        leetcode_handle.scrap_now(uname)
    if platform == 'codechef':
        if codechef_handle is None:
            codechef_handle = get_codechef_handle()
        codechef_handle.scrap_now(uname)