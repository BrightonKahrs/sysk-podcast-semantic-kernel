import os
import uuid
from flask import Blueprint, redirect, session, request, url_for, render_template
from msal import ConfidentialClientApplication

auth_bp = Blueprint('auth', __name__)

allowed_group_ids = ['11670d85-e950-4fa8-9fc9-fd6a00de6af0']

def _build_msal_app():
    return ConfidentialClientApplication(
        os.getenv('CLIENT_ID'),
        authority=os.getenv('AUTHORITY'),
        client_credential=os.getenv('CLIENT_SECRET')
    )


@auth_bp.route('/auth/start')
def auth_start():
    return render_template('login.html')


@auth_bp.route('/login')
def login():
    session['state'] = str(uuid.uuid4())
    auth_url = _build_msal_app().get_authorization_request_url(
        scopes=os.getenv('SCOPE').split(),
        state=session['state'],
        redirect_uri=url_for('auth.authorized', _external=True)
    )
    return redirect(auth_url)

@auth_bp.route('/auth/redirect')
def authorized():
    if request.args.get('state') != session.get('state'):
        return redirect(url_for('auth.login'))

    code = request.args.get('code')
    result = _build_msal_app().acquire_token_by_authorization_code(
        code,
        scopes=os.getenv('SCOPE').split(),
        redirect_uri=url_for('auth.authorized', _external=True)
    )

    if 'id_token_claims' in result:
        claims = result['id_token_claims']
        user_groups = claims.get('groups', [])

        if not any(group_id in allowed_group_ids for group_id in user_groups):
            return "Access denied: you are not authorized.", 403
        
        session['user'] = {
                'name': claims.get('name'),
                'email': claims.get('preferred_username'),
                'user_id': claims.get('oid')
            }
        return redirect(url_for('chat.index'))
    else:
        return f"Login failed: {result.get('error_description')}"

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(
        f"{os.getenv('AUTHORITY')}/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={url_for('auth.login', _external=True)}"
    )
