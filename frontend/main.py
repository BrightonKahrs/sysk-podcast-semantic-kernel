from dotenv import load_dotenv
import os

from flask import Flask

from frontend.routes.chat import chat_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Load config from environment or default
    app.config['BACKEND_URL'] = os.getenv('BACKEND_URL', 'http://localhost:7000')

    # Register blueprints

    app.register_blueprint(chat_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)