from flask_socketio import SocketIO
from flask import  request
from flask_socketio import emit
import json

socketio = SocketIO( cors_allowed_origins='*', async_mode='eventlet')

users={}

@socketio.on('disconnect')
def test_disconnect():
    users.pop(request.sid,'No user found')
    print('Client disconnected')
    print(users)
    
@socketio.on('coneccion')
def test_coneccion(data):
    users[request.sid] = data
    print(users)
    emit('coneccion')
