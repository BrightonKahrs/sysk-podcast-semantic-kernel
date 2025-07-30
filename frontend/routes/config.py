import os

from flask import Blueprint, session, url_for, redirect, jsonify, current_app

from frontend.routes.auth import allowed_group_ids

config_bp = Blueprint('config', __name__)

environment = os.getenv('ENVIRONMENT')

@config_bp.before_request
def require_login():
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.auth_start'))

    user_groups = user.get('groups', [])
    if not any(group_id in allowed_group_ids for group_id in user_groups):
        return "Access denied: you are not authorized.", 403

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