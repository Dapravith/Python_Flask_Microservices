from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)

# Configure the MongoDB settings: the Database URI and the Database Name
app.config["MONGO_URI"] = "mongodb://localhost:172.29.0.2:27017/myDatabase"
mongo = PyMongo(app)

# Reference to the collection
items_collection = mongo.db.items

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing data'}), 400

    item_id = items_collection.insert_one({'name': data['name']}).inserted_id
    new_item = items_collection.find_one({'_id': item_id})
    return jsonify({'id': str(new_item['_id']), 'name': new_item['name']}), 201

@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    try:
        item = items_collection.find_one_or_404({'_id': ObjectId(item_id)})
        return jsonify({'id': str(item['_id']), 'name': item['name']})
    except InvalidId:
        return jsonify({'error': 'Invalid item ID'}), 400

@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing data'}), 400

    try:
        result = items_collection.update_one({'_id': ObjectId(item_id)}, {'$set': {'name': data['name']}})
        if result.matched_count:
            return jsonify({'id': item_id, 'name': data['name']})
        else:
            return jsonify({'error': 'No item found'}), 404
    except InvalidId:
        return jsonify({'error': 'Invalid item ID'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001, host="0.0.0.0")
