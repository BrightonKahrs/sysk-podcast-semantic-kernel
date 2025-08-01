# routes/chat.py
import requests
import uuid
import logging

from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, current_app

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

### Helper Functions ###
def load_user_history_into_session():
    BASE_BACKEND_URL = current_app.config.get('BACKEND_URL')
    user_id = session.get('user', {}).get('user_id')

    if not user_id:
        return {'error': 'User not authenticated'}, 403

    LOAD_URL = f'{BASE_BACKEND_URL}/history'
    chat_res = requests.get(LOAD_URL, headers={'X-User-ID': user_id})

    if chat_res.status_code != 200:
        return {'error': 'Chat backend error'}, 500
    
    session_ids = chat_res.json().get('session_ids')
    session['history_ids'] = session_ids

    return session_ids


### Blueprint functions ###
@chat_bp.before_request
def require_login():
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.auth_start'))

@chat_bp.route('/home', methods=['GET'])
def index():
    if 'session_id' not in session or session.get('session_id') == None:
        session['session_id'] = str(uuid.uuid4())
    if 'conversation' not in session:
        session['conversation'] = []
        load_user_history_into_session()
        
    return render_template(
        'index.html',
        conversation=session.get('conversation', []),
        history_ids=session.get('history_ids', [])
    )

@chat_bp.route('/chat', methods=['POST'])
def chat():
    if 'session_id' not in session or session.get('session_id') == None:
        session['session_id'] = str(uuid.uuid4())
    if 'conversation' not in session:
        session['conversation'] = []

    data = request.get_json()
    prompt = data.get('prompt')
    # prompt = request.form.get('prompt')

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
    
    # If first message / response cycle
    if len(session['conversation']) < 3:
        load_user_history_into_session()

    response_text = chat_res.json().get('response')
    session['conversation'].append({'role': 'assistant', 'content': response_text})
    session.modified = True

    return jsonify({'response': response_text})
    # return redirect(url_for('chat.index'))


@chat_bp.route('/reset', methods=['POST'])
def reset():
    session['conversation'] = []
    session['session_id'] = None
    return redirect(url_for('chat.load_history_all'))


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

@chat_bp.route('/delete/<session_id>', methods=['POST'])
def delete_chat(session_id):
    BASE_BACKEND_URL = current_app.config.get('BACKEND_URL')
    user_id = session.get('user', {}).get('user_id')

    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 403

    DELETE_URL = f'{BASE_BACKEND_URL}/delete/{session_id}'

    chat_res = requests.post(
        DELETE_URL,
        headers={'X-User-ID': user_id}  # 🔒 secure header
    )

    if chat_res.status_code != 200:
        return jsonify({'error': 'Chat backend error'}), 500
    
    return redirect(url_for('chat.load_history_all'))

@chat_bp.route('/history-js', methods=['GET'])
def load_history_for_js():
    result = load_user_history_into_session()

    if isinstance(result, tuple):  # error case returns (dict, status)
        return jsonify(result[0]), result[1]

    # success: result is session_ids list
    return jsonify({"session_ids": result})

@chat_bp.route('/history', methods=['GET'])
def load_history_all():
    result = load_user_history_into_session()

    if isinstance(result, tuple):  # error case returns (dict, status)
        return jsonify(result[0]), result[1]

    # success: result is session_ids list
    return redirect(url_for('chat.index'))