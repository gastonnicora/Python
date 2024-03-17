from flask_socketio import SocketIO
from flask import  request
from flask_socketio import emit
import json
from flask_socketio import join_room, leave_room, send

#agregar en produccion 
socketio = SocketIO( cors_allowed_origins='*')

users={}
@socketio.on('connect')
def test_connect():
    emit('my_response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    users.pop(request.sid,'No user found')
    print('Client disconnected')
    print(users)
    
@socketio.on('coneccion')
def test_coneccion(data):
    users[request.sid] = data

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('joinRoom/'+room, {'data': users[request.sid]}, room= room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    emit('leaveRoom/'+room, {'data': users[request.sid]}, room= room)

def emit_bid(data):
    value = data['value']
    room = data['room']
    emit('bidRoom/'+room, {'data': value}, room= room)

def emit_finish(room):
    emit('finishRoom/'+room, {'data': "finish"}, room= room)

def emit_start(room):
    emit('starthRoom/'+room, {'data': "finish"}, room= room)