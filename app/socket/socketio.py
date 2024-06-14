from flask_socketio import SocketIO
from flask import request
from flask_socketio import emit, join_room, leave_room
import json
import time
from threading import Thread, Lock
import redis

# Conexión a Redis
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

socketio = SocketIO(cors_allowed_origins='*', ping_timeout=60, ping_interval=25)

# Lock para manejar la sincronización
lock = Lock()

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
    print("Usuario se conectó")
    emit('coneccion', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print("Usuario se desconectó")
    with lock:
        del_user(request.sid)
    print(get_users())

@socketio.on_error()
def error_handler(e):
    print('Error:' + str(e))

@socketio.on_error_default
def default_error_handler(e):
    print(f'Default error: {e}')

@socketio.on('borrarUser')
def disconnect(data):
    print("borrarUser")
    with lock:
        set_user(request.sid, {})

@socketio.on('coneccion')
def test_coneccion(data):
    print("Usuario se conectó, datos:")
    print(data)
    with lock:
        set_user(request.sid, data)
    join_room(data["uuid"], request.sid)

@socketio.on('join')
def on_join(data):
    print("join")
    print(data)
    room = data['room']
    join_room(room, request.sid)
    with lock:
        rooms = get_rooms()
        users = get_users()
        if room not in rooms:
            rooms[room] = {"users": [], "time": 0, "timeSet": 0, "bool": True}
        if request.sid in users:
            rooms[room]["users"].append(users[request.sid])
            set_room(room, rooms[room])
    emit('joinToRoom/' + room, rooms[room], room=room)

@socketio.on('leave')
def on_leave(data):
    print("leave")
    print(data)
    room = data['room']
    with lock:
        rooms = get_rooms()
        users = get_users()
        if room in rooms and request.sid in users:
            rooms[room]["users"].remove(users[request.sid])
            set_room(room, rooms[room])
        else:
            print("La sala especificada no existe.")
    leave_room(room, request.sid)
    emit('joinToRoom/' + room, rooms[room], room=room)

def emit_bid(data):
    print("emit bid")
    room = data['room']
    with lock:
        rooms = get_rooms()
        if room in rooms:
            if rooms[room].get("time"):
                print("room")
                print(room)
                reset_countdown(room)
            socketio.emit('bidRoom/' + room, data["bid"], room=room)  # Asumo que data["bid"] es serializable

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
    with lock:
        rooms = get_rooms()
        if room not in rooms:
            rooms[room] = {"users": [], "time": int(time), "timeSet": int(time), "bool": False}
        if not rooms[room].get("bool"):
            rooms[room]["time"] = int(time)
            rooms[room]["timeSet"] = int(time)
            rooms[room]["bool"] = True
            set_room(room, rooms[room])
            thread = Thread(target=countdown_thread, args=(room,))
            thread.start()
    socketio.emit('startRoom/' + room, room=room)

def start(room):
    with lock:
        rooms = get_rooms()
        if room not in rooms:
            rooms[room] = {"users": []}
            set_room(room, rooms[room])
    socketio.emit('startRoom/' + room, room=room)

def countdown_thread(room):
    while True:
        with lock:
            rooms = get_rooms()
            if room not in rooms or rooms[room]["time"] <= 0:
                break
            print("count: " + str(rooms[room]["time"]))
            socketio.emit('countdown/' + room, rooms[room], room=room)
            rooms[room]["time"] -= 1
            set_room(room, rooms[room])
        time.sleep(1)

def reset_countdown(room):
    with lock:
        rooms = get_rooms()
        if room in rooms:
            rooms[room]["time"] = rooms[room]["timeSet"]
            set_room(room, rooms[room])
    print("rooms")
    print(rooms[room]["time"])
