from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from config import DATABASE_URL, SECRET_KEY
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    theme = db.Column(db.String(20), default='dark')

# Meme Model
class Meme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)

# Chat Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/memes', methods=['GET'])
def get_memes():
    memes = Meme.query.all()
    return jsonify([{'id': meme.id, 'url': meme.url, 'category': meme.category} for meme in memes])

@socketio.on('send_message')
def handle_message(data):
    message = Message(sender=data['sender'], text=data['text'])
    db.session.add(message)
    db.session.commit()
    emit('receive_message', {'sender': data['sender'], 'text': data['text']}, broadcast=True)

if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True)
