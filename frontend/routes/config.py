import os

from flask import jsonify, current_app
from flask import Blueprint

config_bp = Blueprint('config', __name__)

environment = os.getenv('ENVIRONMENT')

@config_bp.route('/config')
def get_config():

    if environment == 'local':
        return jsonify({
            'backend_url': 'http://localhost:7000'
        }) 
    else:
        return jsonify({
            'backend_url': current_app.config['BACKEND_URL']
        })