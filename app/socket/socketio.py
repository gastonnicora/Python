from flask_socketio import SocketIO
from flask import  request
from flask_socketio import emit
import json
from flask_socketio import join_room, leave_room, send
import time
from threading import Thread


socketio = SocketIO( cors_allowed_origins='*', ping_timeout=60, ping_interval=25)

users={}
rooms={}
print("socket")
@socketio.on('connect')
def test_connect():
    print("Usuario se conecto")
    emit('coneccion', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print("usuario se desconectado")
    users.pop(request.sid,'No user found')
    print(users)

@socketio.on_error()        # handle all errors
def error_handler(e):
    print('Error:'+str(e))

@socketio.on_error_default  # handle all errors
def default_error_handler(e):
    print(f'Default error: {e}')

@socketio.on('borrarUser')
def disconnect(data):

    print("borrarUser")
    users[request.sid] = {}
    
@socketio.on('coneccion')
def test_coneccion(data):
    print("usuario se conecto, datos:")
    print(data)
    users[request.sid] = data
    join_room(data["uuid"],request.sid)
 
@socketio.on('join')
def on_join(data):
    print("join")
    print(data)
    room = data['room']
    join_room(room,request.sid)
    if not room in rooms:
        rooms[room]= {"users":[], "time":0,"timeSet":0 ,"bool":True}
    rooms[room]["users"].append(users[request.sid])
    emit('joinToRoom/'+room,  rooms[room], room= room)

@socketio.on('leave')
def on_leave(data):
    print("leave")
    print(data)
    room = data['room']
    if room in rooms:
            rooms[room]["users"].remove(users[request.sid])
    else:
        print("La sala especificada no existe.")
    leave_room(room,request.sid)
    emit('joinToRoom/'+room,rooms[room], room= room)

def emit_bid(data):
    print("emit bid")
    room = data['room']
    if  room in rooms:
        if rooms[room].get("time"):
            print("room")
            print(room)
            reset_countdown(room)
        socketio.emit('bidRoom/'+room,data["bid"].toJSON(), room= room)

def emit_finish(room):
    print("emit finish")
    socketio.emit('finishRoom/'+room, {'data': "finish"}, room= room)

@socketio.on('leave_session')
def on_leave_session(data):
    print("leave")
    leave_room(data["uuid"],request.sid)

def emit_updateSesion(data):
    print("update user")
    socketio.emit('updateSession', {'data': data}, room= data["uuid"])

def emit_start(room, time):
    print("start")
    if not room in rooms:
        rooms[room]= {"users":[], "time":int(time),"timeSet":int(time), "bool":False }
    if not rooms[room].get("bool"):
        rooms[room]["time"]= int(time)
        rooms[room]["timeSet"]= int(time)
        thread = Thread(target=countdown_thread, args=(room,))
        thread.start()
        rooms[room]["bool"]=True
    socketio.emit('startRoom/'+room, room= room)

def start(room):
    if not room in rooms:
        rooms[room]= {"users":[]}
    socketio.emit('startRoom/'+room, room= room)

def countdown_thread( room):
    print("count: "+str(rooms[room]["time"]))
    while rooms[room]["time"] > -1:
        socketio.emit('countdown/'+room,rooms[room], room=room)
        rooms[room]["time"] -= 1
        time.sleep(1)

def reset_countdown(room):
    rooms[room]["time"]=rooms[room]["timeSet"]
    print("rooms")
    print(rooms[room]["time"])

