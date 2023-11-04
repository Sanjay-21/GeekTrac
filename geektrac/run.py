from flask import Flask

import os

host = '0.0.0.0'
fallback_port = 5000
if 'PORT' not in os.environ:
    print(f'PORT environment variable not defined.\nUsing fallback port {fallback_port}')
port = int(os.environ.get('PORT', fallback_port))

def create_app():
    app = Flask(__name__)

    from geektrac.views import user_creation
    app.register_blueprint(user_creation)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host = host, port = port)