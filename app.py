from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/items', methods=['POST', 'GET'])
def handle_items():
    if request.method == 'POST':
        data = request.json
        new_item = Item(name=data['name'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'id': new_item.id, 'name': new_item.name}), 201

    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name} for item in items])

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
    app.run(debug=True)
