from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@172.30.0.3:3307/python_app'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
''
@app.before_request
def create_tables():
    db.create_all()

@app.route('/items', methods=['POST'])
def handle_items():
    try:
        data = request.json
        new_item = Item(name=data['name'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'id': new_item.id, 'name': new_item.name}), 201
    except Exception as e:
        return jsonify({'error': e}), 404

@app.route('/items/<int:item_id>', methods=['PUT'])
def handle_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    data = request.json
    item.name = data['name']
    db.session.commit()
    return jsonify({'id': item.id, 'name': item.name})

if __name__ == '__main__':
    app.run(debug=True, port=5001, host="0.0.0.0")
