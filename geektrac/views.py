from flask import Blueprint, request
from werkzeug.security import generate_password_hash


def check_if_user_exists(username):
    return False



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

    if check_if_user_exists(username):
        return "username taken", 409

    print(generate_password_hash(password))
    
    
    return "User success fully created", 200