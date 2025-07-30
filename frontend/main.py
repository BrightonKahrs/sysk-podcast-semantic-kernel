#frontend/main.py
from dotenv import load_dotenv
import os

from flask import Flask, redirect, url_for
from flask_session import Session

from frontend.routes.chat import chat_bp
from frontend.routes.config import config_bp
from frontend.routes.auth import auth_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    # Load config from environment or default
    app.config['BACKEND_URL'] = os.getenv('BACKEND_URL')

    # Register blueprints

    app.register_blueprint(chat_bp)
    app.register_blueprint(config_bp)
    app.register_blueprint(auth_bp)

    @app.route('/')
    def home():
        return redirect(url_for('auth.auth_start'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)