# app.py
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from passlib.hash import pbkdf2_sha256
import hashlib
import os

app = Flask(__name__)
api = Api(app)

# Path to store API keys
API_KEY_FILE = '/app/data/api_keys.txt'


def load_api_keys():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            for line in f:
                key, hashed_key, salt = line.strip().split(',')
                api_keys[key] = (hashed_key, salt)


def save_api_key(key, hashed_key, salt):
    with open(API_KEY_FILE, 'a') as f:
        f.write(f"{key},{hashed_key},{salt}\n")


api_keys = {}
load_api_keys()


def generate_hash(api_key):
    salt = os.urandom(16).hex()
    hashed_key = pbkdf2_sha256.hash(api_key + salt)
    return hashed_key, salt


def verify_hash(api_key, stored_hash, salt):
    return pbkdf2_sha256.verify(api_key + salt, stored_hash)


class AdminAPI(Resource):
    def put(self):
        data = request.get_json()
        api_key = data.get('api_key')
        if not api_key:
            return {"message": "API key required"}, 400
        hashed_key, salt = generate_hash(api_key)
        api_keys[api_key] = (hashed_key, salt)
        save_api_key(api_key, hashed_key, salt)
        return {"message": "API key added"}, 201

    def delete(self):
        data = request.get_json()
        api_key = data.get('api_key')
        if not api_key:
            return {"message": "API key required"}, 400
        if api_key in api_keys:
            del api_keys[api_key]
            # Rewrite the file without the deleted key
            with open(API_KEY_FILE, 'w') as f:
                for key, (hashed_key, salt) in api_keys.items():
                    f.write(f"{key},{hashed_key},{salt}\n")
            return {"message": "API key deleted"}, 200
        return {"message": "API key not found"}, 404

    def get(self):
        # Return a list of hashed API keys
        hashed_keys = [hashed_key for _, (hashed_key, _) in api_keys.items()]
        return jsonify(hashed_keys)


class ValidateAPI(Resource):
    def get(self):
        api_key = request.args.get('api_key')
        if not api_key:
            return {"message": "API key required"}, 400
        for key, (stored_hash, salt) in api_keys.items():
            if verify_hash(api_key, stored_hash, salt):
                return {"message": "Accepted"}, 200
        return {"message": "Denied"}, 403


api.add_resource(AdminAPI, '/admin')
api.add_resource(ValidateAPI, '/validate')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
