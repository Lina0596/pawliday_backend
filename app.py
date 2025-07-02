from flask import Flask, jsonify, request
from flask_cors import CORS
from datahandler.sqlite_handler import SQLiteHandler
from exceptions import NotFoundError, InvalidInputError, DatabaseError
from imagekitio import ImageKit
from dotenv import load_dotenv
import os


app = Flask(__name__)
CORS(app)


data_manager = SQLiteHandler('pawliday.db')


load_dotenv()

imagekit = ImageKit(
    public_key=os.environ['IMAGEKIT_PUBLIC_KEY'],
    private_key=os.environ['IMAGEKIT_PRIVATE_KEY'],
    url_endpoint=os.environ['IMAGEKIT_URL_ENDPOINT']
)


@app.route('/api/wakeup', methods=['GET'])
def server_wakeup():
    return jsonify({"message": "Server awake"}), 200


@app.route('/api/auth-params', methods=['GET'])
def get_auth_params():
    auth_params = imagekit.get_authentication_parameters()
    return jsonify(auth_params)


@app.route('/api/sitters', methods=['GET'])
def get_all_sitters():
    sitters = data_manager.get_all_sitters()
    return jsonify(sitters), 200
    

@app.route('/api/sitters/<sitter_id>', methods=['GET'])
def get_sitter(sitter_id):
    sitter = data_manager.get_sitter(sitter_id=sitter_id)
    return jsonify(sitter), 200


@app.route('/api/sitters', methods=['GET', 'POST'])
def add_sitter():
    if request.method == 'POST':
        new_sitter_data = request.get_json()
        data_manager.add_sitter(new_sitter_data=new_sitter_data)
        return jsonify({"message": "Sitter successfully added"}), 201
    sitters = data_manager.get_all_sitters()
    return jsonify(sitters), 200


@app.route('/api/sitters/<sitter_id>', methods=['PUT'])
def update_sitter(sitter_id):
    updated_data = request.get_json()
    data_manager.update_sitter(sitter_id=sitter_id, updated_data=updated_data)
    return jsonify({"message": "Sitter successfully updated"}), 200


@app.route('/api/sitters/<sitter_id>/owners', methods=['GET'])
def get_all_owners(sitter_id):
    owners = data_manager.get_all_owners(sitter_id)
    return jsonify(owners), 200


@app.route('/api/sitters/<sitter_id>/owners/<owner_id>', methods=['GET'])
def get_owner(sitter_id, owner_id):
    owner = data_manager.get_owner(sitter_id=sitter_id, owner_id=owner_id)
    return jsonify(owner), 200


@app.route('/api/sitters/<sitter_id>/owners', methods=['GET', 'POST'])
def add_owner(sitter_id):
    if request.method == 'POST':
        new_owner_data = request.get_json()
        created_owner = data_manager.add_owner(sitter_id=sitter_id, new_owner_data=new_owner_data)
        return jsonify(created_owner), 201
    owners = data_manager.get_all_owners(sitter_id)
    return jsonify(owners), 200


@app.route('/api/sitters/<sitter_id>/owners/<owner_id>', methods=['PUT'])
def update_owner(sitter_id, owner_id):
    updated_data = request.get_json()
    data_manager.update_owner(sitter_id=sitter_id, owner_id=owner_id, updated_data=updated_data)
    return jsonify({"message": f"Owner successfully updated"}), 200


@app.route('/api/sitters/<sitter_id>/owners/<owner_id>', methods=['DELETE'])
def delete_owner(sitter_id, owner_id):
    data_manager.delete_owner(sitter_id=sitter_id, owner_id=owner_id)
    return jsonify({"message": "Owner and associated dogs successfully deleted"}), 200


@app.route('/api/sitters/<sitter_id>/owners/<owner_id>/dogs', methods=['GET'])
def get_owner_dogs(sitter_id, owner_id):
    owner_dogs = data_manager.get_owner_dogs(sitter_id=sitter_id, owner_id=owner_id)
    return jsonify(owner_dogs), 200


@app.route('/api/sitters/<sitter_id>/owners/<owner_id>/dogs', methods=['GET', 'POST'])
def add_dog(sitter_id, owner_id):
    if request.method == 'POST':
        new_dog_data = request.get_json()
        created_dog = data_manager.add_dog(sitter_id=sitter_id, owner_id=owner_id, new_dog_data=new_dog_data)
        return jsonify(created_dog), 201
    owner_dogs = data_manager.get_owner_dogs(owner_id)
    return jsonify(owner_dogs), 200


@app.route('/api/sitters/<sitter_id>/dogs', methods=['GET'])
def get_all_dogs(sitter_id):
    dogs = data_manager.get_all_dogs(sitter_id=sitter_id)
    return jsonify(dogs), 200


@app.route('/api/sitters/<sitter_id>/dogs/<dog_id>', methods=['GET'])
def get_dog(sitter_id, dog_id):
    dog = data_manager.get_dog(sitter_id=sitter_id, dog_id=dog_id)
    return jsonify(dog), 200


@app.route('/api/sitters/<sitter_id>/dogs/<dog_id>', methods=['PUT'])
def update_dog(sitter_id, dog_id):
    updated_data = request.get_json()
    data_manager.update_dog(sitter_id=sitter_id, dog_id=dog_id, updated_data=updated_data)
    return jsonify({"message": "Dog successfully updated"}), 200


@app.route('/api/sitters/<sitter_id>/dogs/<dog_id>', methods=['DELETE'])
def delete_dog(sitter_id, dog_id):
    data_manager.delete_dog(sitter_id=sitter_id, dog_id=dog_id)
    return jsonify({"message": f"Dog successfully deleted"}), 200
    

@app.errorhandler(NotFoundError)
def handle_not_found(e):
    return jsonify({"error": str(e)}), 404


@app.errorhandler(InvalidInputError)
def handle_invalid_input(e):
    return jsonify({"error": str(e)}), 400


@app.errorhandler(DatabaseError)
def handle_db_error(e):
    return jsonify({"error": str(e)}), 503


if __name__ == '__main__':
    app.run(debug=True)
