from app.main import bp as app
from flask import jsonify, request, send_from_directory

@app.route('/', methods=['GET'])
def test():
    return jsonify("Si ves esto, quiero que sepas que me pude titular :)"), 200

@app.route('/static/<path:path>')
def static_file(path):
    return send_from_directory('static', path)