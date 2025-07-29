from flask import jsonify, current_app

@app.route('/config')
def get_config():
    return jsonify({
        'backend_url': current_app.config['BACKEND_URL']
    })