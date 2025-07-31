# routes/chat.py
import requests
import uuid

from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, current_app

chat_bp = Blueprint('chat', __name__)

@chat_bp.before_request
def require_login():
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.auth_start'))

@chat_bp.route('/home', methods=['GET'])
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    if 'conversation' not in session:
        session['conversation'] = []
    return render_template('index.html', conversation=session['conversation'])

@chat_bp.route('/chat', methods=['POST'])
def chat():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    if 'conversation' not in session:
        session['conversation'] = []

    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    session['conversation'].append({'role': 'user', 'content': prompt})

    BASE_BACKEND_URL = current_app.config.get('BACKEND_URL')
    CHAT_URL = f'{BASE_BACKEND_URL}/chat'

    chat_res = requests.post(
        CHAT_URL,
        json={
            'session_id': session.get('session_id'),
            'prompt': prompt
            },
        headers={
            'X-User-ID': session.get('user', {}).get('user_id'),
        }
    )

    if chat_res.status_code != 200:
        return jsonify({'error': 'Chat backend error'}), 500

    response_text = chat_res.json().get('response')
    session['conversation'].append({'role': 'assistant', 'content': response_text})
    session.modified = True

    return jsonify({'response': response_text})

@chat_bp.route('/reset', methods=['POST'])
def reset():
    BASE_BACKEND_URL = current_app.config.get('BACKEND_URL')
    SESSION_RESET_URL = f'{BASE_BACKEND_URL}/reset_session'

    requests.post(
        SESSION_RESET_URL,
        json={'session_id': session['session_id']},
        headers={'X-User-ID': session.get('user', {}).get('user_id')}
    )
    session['conversation'] = []
    return redirect(url_for('chat.index'))

@chat_bp.route('/history/<session_id>', methods=['GET'])
def load_chat(session_id):
    BASE_BACKEND_URL = current_app.config.get('BACKEND_URL')
    user_id = session.get('user', {}).get('user_id')

    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 403

    LOAD_URL = f'{BASE_BACKEND_URL}/history/{session_id}'

    chat_res = requests.get(
        LOAD_URL,
        headers={'X-User-ID': user_id}  # 🔒 secure header
    )

    if chat_res.status_code != 200:
        return jsonify({'error': 'Chat backend error'}), 500

    session['session_id'] = chat_res.json().get('session_id')
    session['conversation'] = chat_res.json().get('history')
    
    return redirect(url_for('chat.index'))
