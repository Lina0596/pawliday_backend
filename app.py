from flask import Flask, jsonify, request
from flask_cors import CORS
from datahandler.sqlite_handler import SQLiteHandler


app = Flask(__name__)
CORS(app)


data_manager = SQLiteHandler('pawliday.db')


@app.route('/api/owners', methods=['GET'])
def get_all_owners():
    owners = data_manager.get_all_owners()
    return jsonify(owners)


@app.route('/api/owners/<int:owner_id>', methods=['DELETE'])
def delete_owner(owner_id):
    data_manager.delete_owner(owner_id=owner_id)
    return jsonify({"message": f"Owner and dogs with owner id {owner_id} successfully deleted."}), 200


@app.route('/api/owner_dogs/<int:owner_id>', methods=['GET'])
def get_owner_dogs(owner_id):
    owner_dogs = data_manager.get_owner_dogs(owner_id)
    return jsonify(owner_dogs)


@app.route('/api/dog/<int:dog_id>', methods=['GET'])
def get_dog(dog_id):
    dog = data_manager.get_dog(dog_id)
    return jsonify(dog)


@app.route('/api/dog/<int:dog_id>', methods=['DELETE'])
def delete_dog(dog_id):
    data_manager.delete_dog(dog_id=dog_id)
    return jsonify({"message": f"Dog with id {dog_id} successfully deleted."}), 200


if __name__ == '__main__':
    app.run(debug=True)
