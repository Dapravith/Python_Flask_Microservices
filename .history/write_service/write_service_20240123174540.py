from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.utils import url_quote
# app = Flask(__name__)
from werkzeug.utils import url_quote  # Import url_quote from werkzeug.utils

app = Flask(__name__)
# Update the MySQL connection string
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root@172.18.0.2:3306/cloud_computing' 
# Disable the Flask-SQLAlchemy track modifications feature to suppress a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/items', methods=['POST'])
def handle_items():
    data = request.json
    new_item = Item(name=data['name'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'id': new_item.id, 'name': new_item.name}), 201

@app.route('/items/<int:item_id>', methods=['PUT', 'DELETE'])
def handle_item(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == 'PUT':
        data = request.json
        item.name = data['name']
        db.session.commit()
        return jsonify({'id': item.id, 'name': item.name})

    db.session.delete(item)
    db.session.commit()
    return jsonify({}), 204

if __name__ == '__main__':
    app.run(debug=True, port=5000,host="0.0.0.0")
