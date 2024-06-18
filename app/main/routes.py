from app.main import bp as app
from flask import jsonify, request

@app.route('', methods=['GET'])
def test():
    return jsonify("Si ves esto, quiero que sepas que me pude titular :)"), 200