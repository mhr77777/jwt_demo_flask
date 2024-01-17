from flask import Flask, jsonify, request
import jwt
import datetime
import dotenv
app = Flask(__name__)

app.config['SECRET_KEY'] = dotenv.get_key("./.env","SECRET_KEY")

@app.route("/")
def index():
    frnt_f = open("front.html")
    frnt = frnt_f.read()
    frnt_f.close()
    return frnt

@app.route('/gen_token', methods=['POST'])
def generate_token():
    
    rbody = request.data

    if not request.is_json:
        return jsonify({"error": "Missing data in request"}), 400

    username = request.json.get('username')
    password = request.json.get('password')

    if username != "garfield" or password != "lasagna":
        return jsonify({"error": "Invalid authentication data"}), 400

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
        'iat': datetime.datetime.utcnow(),
        'sub': 'garfield'
    }

    # Generate a token
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token})

@app.route('/auth_check', methods=['POST'])
def check_auth():
    token = request.json.get('token', None)
    if not token:
        return jsonify({"error": "Token is missing"}), 400
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return jsonify({"authstatus": 1}), 200
    except ExpiredSignatureError:
        return jsonify({"authstatus": 0}), 401
    except InvalidTokenError:
        return jsonify({"authstatus": 0}), 401

if __name__ == "__main__":
  app.run()