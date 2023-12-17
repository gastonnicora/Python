from flask_socketio import SocketIO
from flask import  request
from flask_socketio import emit
import json

#agregar en produccion 
socketio = SocketIO( cors_allowed_origins='*')

users={}
@socketio.on('connect')
def test_connect():
    print(users)
    print("conectado")
    emit('my_response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    users.pop(request.sid,'No user found')
    print('Client disconnected')
    print(users)
    
@socketio.on('coneccion')
def test_coneccion(data):
    users[request.sid] = data
    print(users)
#     emit('coneccion', {}) 