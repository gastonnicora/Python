from flask_socketio import SocketIO
from flask import  request
from flask_socketio import emit
import json
from flask_socketio import join_room, leave_room, send
import time
from threading import Thread


socketio = SocketIO( cors_allowed_origins='*')

users={}
rooms={}
@socketio.on('connect')
def test_connect():
    emit('coneccion', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    users.pop(request.sid,'No user found')
    print(users)

@socketio.on('borrarUser')
def disconnect(data):
    users.pop(request.sid,'No user found')
    print(users)
    
@socketio.on('coneccion')
def test_coneccion(data):
    users[request.sid] = data
 
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room,request.sid)
    if not room in rooms:
        rooms[room]= {"users":[], "time":0,"timeSet":0 ,"bool":True}
    rooms[room]["users"].append(users[request.sid])
    emit('joinToRoom/'+room,  rooms[room], room= room)

@socketio.on('leave')
def on_leave(data):
    print("leave")
    room = data['room']
    if room in rooms:
            rooms[room]["users"].remove(users[request.sid])
    else:
        print("La sala especificada no existe.")
    leave_room(room,request.sid)
    emit('joinToRoom/'+room,rooms[room], room= room)

def emit_bid(data):
    room = data['room']
    reset_countdown(room)
    socketio.emit('bidRoom/'+room,data["bid"].toJSON(), room= room)

def emit_finish(room):
    socketio.emit('finishRoom/'+room, {'data': "finish"}, room= room)

@socketio.on('leave_session')
def on_leave_session(data):
    leave_room(data.uuid,request.sid)

def emit_updateSesion(data):
    socketio.emit('updateSession/'+data.uuid, {'data': data}, room= data.uuid)

def emit_start(room, time):
    if not room in rooms:
        rooms[room]= {"users":[], "time":time,"timeSet":time, "bool":False }
    rooms[room]["time"]= time
    rooms[room]["timeSet"]= time
    if not rooms[room]["bool"]:
        thread = Thread(target=countdown_thread, args=(room,))
        thread.start()
        rooms[room]["bool"]=True
    socketio.emit('startRoom/'+room, room= room)

def countdown_thread( room):
    while rooms[room]["time"] > -1:
        print(rooms[room]["time"])
        socketio.emit('countdown/'+room,rooms[room], room=room)
        time.sleep(1)
        rooms[room]["time"] -= 1

def reset_countdown(room):
    rooms[room]["time"]=rooms[room]["timeSet"]

