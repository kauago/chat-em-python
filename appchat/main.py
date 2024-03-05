from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seu_secrety_key'
socketio = SocketIO(app)

# Dicionário de salas e mensagens
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    if room not in rooms:
        rooms[room] = []
    rooms[room].append({'username': username, 'message': 'entrou na sala.'})
    socketio.emit('message', {'room': room, 'messages': rooms[room]}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    if room in rooms:
        rooms[room].append({'username': username, 'message': 'saiu da sala.'})
        socketio.emit('message', {'room': room, 'messages': rooms[room]}, room=room)
        if not rooms[room]:
            del rooms[room]

@socketio.on('message')
def handle_message(data):
    username = data['username']
    room = data['room']
    message = data['message']
    if room in rooms:
        rooms[room].append({'username': username, 'message': message})
        socketio.emit('message', {'room': room, 'messages': rooms[room]}, room=room)

if __name__ == '__main__':
    socketio.run(app)
