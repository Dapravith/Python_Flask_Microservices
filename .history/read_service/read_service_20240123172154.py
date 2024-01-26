from flask import Flask, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)

# Configure the MongoDB settings: the Database URI and the Database Name
app.config["MONGO_URI"] = "mongodb://localhost:172.29.0.2:27017/myDatabase"
mongo = PyMongo(app)

# Reference to the collection
items_collection = mongo.db.items

@app.route('/items', methods=['GET'])
def get_items():
    items = items_collection.find({})
    # Using dumps from bson.json_util to convert cursor to JSON directly
    return dumps(items), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002, host="0.0.0.0")
