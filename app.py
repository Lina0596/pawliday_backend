from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, get_jwt_identity, get_csrf_token, get_jwt
from functools import wraps
from datahandler.sqlite_handler import SQLiteHandler
from exceptions import NotFoundError, InvalidInputError, DatabaseError
from imagekitio import ImageKit
from dotenv import load_dotenv
import os


app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5174", "http://localhost:5173", "https://pawliday-frontend.onrender.com"])
data_manager = SQLiteHandler('pawliday.db')


load_dotenv()


app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_HTTPONLY'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'None'


jwt = JWTManager(app)


imagekit = ImageKit(
    public_key=os.environ.get('IMAGEKIT_PUBLIC_KEY'),
    private_key=os.environ.get('IMAGEKIT_PRIVATE_KEY'),
    url_endpoint=os.environ.get('IMAGEKIT_URL_ENDPOINT')
)


@app.route('/api/wakeup', methods=['GET'])
def server_wakeup():
    return jsonify({"message": "Server awake"}), 200


@app.route('/api/auth-params', methods=['GET'])
def get_auth_params():
    auth_params = imagekit.get_authentication_parameters()
    return jsonify(auth_params)


@app.route('/api/login', methods=['POST'])
def login():
    login_data = request.get_json()
    sitter = data_manager.authenticate_sitter(login_data=login_data)
    access_token = create_access_token(identity=str(sitter['sitter_id']))
    csrf_token = get_csrf_token(access_token)
    response = jsonify({"message": "Login successfully", "csrf_token": csrf_token})
    set_access_cookies(response, access_token)
    return response, 200


@app.route('/api/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logout successfully"})
    unset_jwt_cookies(response)
    return response, 200


@app.route('/api/registration', methods=['POST'])
def registration():
    new_sitter_data = request.get_json()
    data_manager.add_sitter(new_sitter_data=new_sitter_data)
    return jsonify({"message": "Registration successfully"}), 201
    

@app.route('/api/sitter', methods=['GET'])
@jwt_required()
def get_sitter():
    sitter_id = get_jwt_identity()
    sitter = data_manager.get_sitter(sitter_id=sitter_id)
    csrf_token = get_jwt()["csrf"]
    response = jsonify({"sitter": sitter, "csrf_token": csrf_token})
    return response, 200


@app.route('/api/sitter/update', methods=['PUT'])
@jwt_required()
def update_sitter():
    sitter_id = get_jwt_identity()
    updated_data = request.get_json()
    updated_sitter = data_manager.update_sitter(sitter_id=sitter_id, updated_data=updated_data)
    csrf_token = get_jwt()["csrf"]
    response = jsonify({"sitter": updated_sitter, "message": "Sitter profile successfully updated", "csrf_token": csrf_token})
    return response, 200


@app.route('/api/sitter/delete', methods=['DELETE'])
@jwt_required()
def delete_sitter():
    sitter_id = get_jwt_identity()
    data_manager.delete_sitter(sitter_id=sitter_id)
    response = jsonify({"message": "Sitter profile successfully deleted"})
    unset_jwt_cookies(response)
    return response, 200


@app.route('/api/sitter/owners', methods=['GET'])
@jwt_required()
def get_all_owners():
    sitter_id = get_jwt_identity()
    owners = data_manager.get_all_owners(sitter_id=sitter_id)
    csrf_token = get_jwt()["csrf"]
    response = jsonify({"owners": owners, "csrf_token": csrf_token})
    return response, 200


@app.route('/api/sitter/owners/<owner_id>', methods=['GET'])
@jwt_required()
def get_owner(owner_id):
    sitter_id = get_jwt_identity()
    owner = data_manager.get_owner(sitter_id=sitter_id, owner_id=owner_id)
    csrf_token = get_jwt()["csrf"]
    response = jsonify({"owner": owner, "csrf_token": csrf_token})
    return response, 200


@app.route('/api/sitters/owners/add', methods=['GET', 'POST'])
@jwt_required()
def add_owner():
    sitter_id = get_jwt_identity()
    csrf_token = get_jwt()["csrf"]
    if request.method == 'POST':
        new_owner_data = request.get_json()
        created_owner = data_manager.add_owner(sitter_id=sitter_id, new_owner_data=new_owner_data)
        response = jsonify({"owner": created_owner, "csrf_token": csrf_token})
        return response, 201
    owners = data_manager.get_all_owners(sitter_id)
    response = jsonify({"owners": owners, "csrf_token": csrf_token})
    return response, 200


@app.route('/api/sitter/owners/<owner_id>/update', methods=['PUT'])
@jwt_required()
def update_owner(owner_id):
    sitter_id = get_jwt_identity()
    updated_data = request.get_json()
    data_manager.update_owner(sitter_id=sitter_id, owner_id=owner_id, updated_data=updated_data)
    csrf_token = get_jwt()["csrf"]
    response = jsonify({"message": "Owner successfully updated", "csrf_token": csrf_token})
    return response, 200


@app.route('/api/sitter/owners/<owner_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_owner(owner_id):
    sitter_id = get_jwt_identity()
    data_manager.delete_owner(sitter_id=sitter_id, owner_id=owner_id)
    csrf_token = get_jwt()["csrf"]
    response = jsonify({"message": "Owner and associated dogs successfully deleted", "csrf_token": csrf_token})
    return response, 200


@app.route('/api/sitter/dogs', methods=['GET'])
@jwt_required()
def get_all_dogs():
    sitter_id = get_jwt_identity()
    dogs = data_manager.get_all_dogs(sitter_id=sitter_id)
    csrf_token = get_jwt()["csrf"]
    response = jsonify({"dogs": dogs, "csrf_token": csrf_token})
    return response, 200


@app.route('/api/sitter/dogs/<dog_id>', methods=['GET'])
@jwt_required()
def get_dog(dog_id):
    sitter_id = get_jwt_identity()
    dog = data_manager.get_dog(sitter_id=sitter_id, dog_id=dog_id)
    csrf_token = get_jwt()["csrf"]
    response = jsonify({"dog": dog, "csrf_token": csrf_token})
    return response, 200
    

@app.route('/api/sitter/owners/<owner_id>/dogs/add', methods=['GET', 'POST'])
@jwt_required()
def add_dog(owner_id):
    sitter_id = get_jwt_identity()
    csrf_token = get_jwt()["csrf"]
    if request.method == 'POST':
        new_dog_data = request.get_json()
        created_dog = data_manager.add_dog(sitter_id=sitter_id, owner_id=owner_id, new_dog_data=new_dog_data)
        response = jsonify({"dog": created_dog, "csrf_token": csrf_token})
        return response, 201
    owner_dogs = data_manager.get_owner_dogs(owner_id)
    response = jsonify({"owner_dogs": owner_dogs, "csrf_token": csrf_token})
    return response, 200


@app.route('/api/sitter/dogs/<dog_id>/update', methods=['PUT'])
@jwt_required()
def update_dog(dog_id):
    sitter_id = get_jwt_identity()
    updated_data = request.get_json()
    data_manager.update_dog(sitter_id=sitter_id, dog_id=dog_id, updated_data=updated_data)
    csrf_token = get_jwt()["csrf"]
    response = jsonify({"message": "Dog successfully updated", "csrf_token": csrf_token})
    return response, 200


@app.route('/api/sitter/dogs/<dog_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_dog(dog_id):
    sitter_id = get_jwt_identity()
    data_manager.delete_dog(sitter_id=sitter_id, dog_id=dog_id)
    csrf_token = get_jwt()["csrf"]
    response = jsonify({"message": "Dog successfully deleted", "csrf_token": csrf_token})
    return response, 200


@app.route('/api/sitter/owners/<owner_id>/dogs', methods=['GET'])
@jwt_required()
def get_owner_dogs(owner_id):
    sitter_id = get_jwt_identity()
    owner_dogs = data_manager.get_owner_dogs(sitter_id=sitter_id, owner_id=owner_id)
    csrf_token = get_jwt()["csrf"]
    response = jsonify({"owner_dogs": owner_dogs, "csrf_token": csrf_token})
    return response, 200
    

@app.errorhandler(NotFoundError)
def handle_not_found(e):
    return jsonify({"error": str(e)}), 404


@app.errorhandler(InvalidInputError)
def handle_invalid_input(e):
    return jsonify({"error": str(e)}), 400


@app.errorhandler(DatabaseError)
def handle_db_error(e):
    return jsonify({"error": str(e)}), 503


@jwt.unauthorized_loader
def handle_missing_token(e):
    return jsonify({"error": "Please Login"}), 401


@jwt.invalid_token_loader
def handle_invalid_token(e):
    return jsonify({"error": "Please Login"}), 401


@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    return jsonify({"error": "Please Login"}), 401


if __name__ == '__main__':
    app.run(debug=True)
