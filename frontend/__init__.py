# flask_app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes.chat import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')

    return app
