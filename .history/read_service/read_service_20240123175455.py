from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import url_quote  # Import url_quote from werkzeug.utils

app = Flask(__name__)

# app = Flask(__name__)
# Update the MySQL connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@172.18.0.2:3306/python_app' 
# Disable the Flask-SQLAlchemy track modifications feature to suppress a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/items', methods=['GET'])
def handle_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name} for item in items])

if __name__ == '__main__':
    app.run(debug=True, port=5001,host="0.0.0.0")
