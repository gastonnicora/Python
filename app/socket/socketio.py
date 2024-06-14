from flask_socketio import SocketIO
from flask import request
from flask_socketio import emit, join_room, leave_room, send
import json
import time
from threading import Thread
import redis

# Conexión a Redis
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

socketio = SocketIO(cors_allowed_origins='*', ping_timeout=60, ping_interval=25)

def get_users():
    users = redis_client.hgetall('users')
    return {k: json.loads(v) for k, v in users.items()}

def set_user(sid, data):
    redis_client.hset('users', sid, json.dumps(data))

def del_user(sid):
    redis_client.hdel('users', sid)

def get_rooms():
    rooms = redis_client.hgetall('rooms')
    return {k: json.loads(v) for k, v in rooms.items()}

def set_room(room, data):
    redis_client.hset('rooms', room, json.dumps(data))

def del_room(room):
    redis_client.hdel('rooms', room)

print("socket")
@socketio.on('connect')
def test_connect():
    print("Usuario se conecto")
    emit('coneccion', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print("usuario se desconectado")
    del_user(request.sid)
    print(get_users())

@socketio.on_error()        # handle all errors
def error_handler(e):
    print('Error:' + str(e))

@socketio.on_error_default  # handle all errors
def default_error_handler(e):
    print(f'Default error: {e}')

@socketio.on('borrarUser')
def disconnect(data):
    print("borrarUser")
    set_user(request.sid, {})

@socketio.on('coneccion')
def test_coneccion(data):
    print("usuario se conecto, datos:")
    print(data)
    set_user(request.sid, data)
    join_room(data["uuid"], request.sid)

@socketio.on('join')
def on_join(data):
    print("join")
    print(data)
    room = data['room']
    join_room(room, request.sid)
    rooms = get_rooms()
    if room not in rooms:
        rooms[room] = {"users": [], "time": 0, "timeSet": 0, "bool": True}
    rooms[room]["users"].append(get_users()[request.sid])
    set_room(room, rooms[room])
    emit('joinToRoom/' + room, rooms[room], room=room)

@socketio.on('leave')
def on_leave(data):
    print("leave")
    print(data)
    room = data['room']
    rooms = get_rooms()
    if room in rooms:
        rooms[room]["users"].remove(get_users()[request.sid])
        set_room(room, rooms[room])
    else:
        print("La sala especificada no existe.")
    leave_room(room, request.sid)
    emit('joinToRoom/' + room, rooms[room], room=room)

def emit_bid(data):
    print("emit bid")
    room = data['room']
    rooms = get_rooms()
    if room in rooms:
        if rooms[room].get("time"):
            reset_countdown(room)
        socketio.emit('bidRoom/' + room, data["bid"].toJSON(), room=room)

def emit_finish(room):
    print("emit finish")
    socketio.emit('finishRoom/' + room, {'data': "finish"}, room=room)

@socketio.on('leave_session')
def on_leave_session(data):
    print("leave")
    leave_room(data["uuid"], request.sid)

def emit_updateSesion(data):
    print("update user")
    socketio.emit('updateSession', {'data': data}, room=data["uuid"])

def emit_start(room, time):
    print("start")
    rooms = get_rooms()
    if room not in rooms:
        rooms[room] = {"users": [], "time": int(time), "timeSet": int(time), "bool": False}
    rooms[room]["time"] = int(time)
    rooms[room]["timeSet"] = int(time)
    set_room(room, rooms[room])
    if not rooms[room].get("bool"):
        thread = Thread(target=countdown_thread, args=(room,))
        thread.start()
        rooms[room]["bool"] = True
        set_room(room, rooms[room])
    socketio.emit('startRoom/' + room, room=room)

def start(room):
    if room not in get_rooms():
        set_room(room, {"users": []})
    socketio.emit('startRoom/' + room, room=room)

def countdown_thread(room):
    rooms = get_rooms()
    print("count: " + str(rooms[room]["time"]))
    while rooms[room]["time"] > -1:
        socketio.emit('countdown/' + room, rooms[room], room=room)
        time.sleep(1)
        rooms[room]["time"] -= 1
        set_room(room, rooms[room])

def reset_countdown(room):
    rooms = get_rooms()
    rooms[room]["time"] = rooms[room]["timeSet"]
    set_room(room, rooms[room])
