from flask_socketio import SocketIO
from flask import request
from flask_socketio import emit, join_room, leave_room
import time
from threading import Thread
import logging
import redis
import os

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

socketio = SocketIO(cors_allowed_origins='*',async_mode='eventlet', 
                    message_queue=f'redis://{redis_host}:6379/0', ping_timeout=60, ping_interval=25, logger=True, engineio_logger=True)


def add_user(sid, data):
    redis_client.hmset(sid, data)

def get_user(sid):
    return redis_client.hgetall(sid)

def remove_user(sid):
    redis_client.delete(sid)

def add_room(room):
    if not redis_client.exists(room):
        redis_client.hmset(room, {"users": "", "time": 0, "timeSet": 0, "bool": False})

def update_room(room, data):
    redis_client.hmset(room, data)

def get_room(room):
    return redis_client.hgetall(room)

def remove_room(room):
    redis_client.delete(room)

@socketio.on('connect')
def test_connect():
    logging.info("coneccion")
    emit('connect', {'data': 'Connected'})
    logging.info("conectado")

@socketio.on('disconnect')
def test_disconnect():
    try:
        logging.info("Desconexión de: %s", request.sid)
        user_data = get_user(request.sid)
        if user_data:
            room = user_data.get(b"room")
            if room:
                room = room.decode()
                leave_room(room)
                current_room = get_room(room)
                if current_room:
                    updated_users = current_room[b"users"].decode().split(",")
                    updated_users.remove(user_data[b"uuid"].decode())
                    updated_users = ",".join(updated_users)
                    update_room(room, {"users": updated_users})
                remove_user(request.sid)
                logging.info("Usuario %s desconectado y eliminado de la lista.", request.sid)
    except Exception as e:
        logging.error("Error en desconexión: %s", str(e))

@socketio.on_error()
def error_handler(e):
    event_name = request.event if hasattr(request, 'event') else 'unknown event'
    error_message = str(e)
    logging.error(f"Error en la conexión {request.sid} en el evento '{event_name}': {error_message}")

@socketio.on_error_default
def default_error_handler(e):
    logging.error(f'Default error: {e}')

@socketio.on('borrarUser')
def disconnect(data):
    logging.info("borrar user")
    remove_user(request.sid)

@socketio.on('coneccion')
def test_coneccion(data):
    logging.info("usuario conectado")
    try:
        if data:
            add_user(request.sid, data)
            join_room(data["uuid"])
            add_room(data["uuid"])
            logging.info("coneccion data:")
            logging.info(data)
    except Exception as e:
        logging.error("coneccion")
        error_handler(e)

@socketio.on('join')
def on_join(data):
    try:
        logging.info("join")
        room = data['room']
        join_room(room)
        user_data = get_user(request.sid)
        if user_data:
            current_room = get_room(room)
            if current_room:
                users_list = current_room[b"users"].decode().split(",") if current_room[b"users"] else []
                users_list.append(user_data[b"uuid"].decode())
                update_room(room, {"users": ",".join(users_list)})
                emit('joinToRoom/' + room, current_room, room=room)
    except Exception as e:
        logging.error("join")
        error_handler(e)

@socketio.on('leave')
def on_leave(data):
    logging.info("leave")
    room = data['room']
    leave_room(room)
    user_data = get_user(request.sid)
    if user_data:
        current_room = get_room(room)
        if current_room:
            updated_users = current_room[b"users"].decode().split(",")
            updated_users.remove(user_data[b"uuid"].decode())
            update_room(room, {"users": ",".join(updated_users)})
            emit('joinToRoom/' + room, current_room, room=room)

def emit_bid(data):
    logging.info("emit bid")
    room = data['room']
    current_room = get_room(room)
    if current_room and int(current_room[b"time"]) >= 0:
        reset_countdown(room)
    socketio.emit('bidRoom/' + room, data["bid"], room=room)

def emit_finish(room):
    logging.info("emit finish")
    socketio.emit('finishRoom/' + room, {'data': "finish"}, room=room)

@socketio.on('leave_session')
def on_leave_session(data):
    logging.info("leave")
    leave_room(data["uuid"], request.sid)

def emit_updateSesion(data):
    logging.info("update session")
    socketio.emit('updateSession', {'data': data}, room=data["uuid"])

def emit_start(room, time):
    logging.info("emit start")
    add_room(room)
    current_room = get_room(room)
    if not current_room[b"bool"]:
        update_room(room, {"time": int(time), "timeSet": int(time), "bool": True})
        thread = Thread(target=countdown_thread, args=(room,))
        thread.start()
    socketio.emit('startRoom/' + room, room=room)
def start(room):
    logging.info("start")
    current_room = get_room(room)
    if not current_room:
         update_room(room, {"users": []})
    socketio.emit('startRoom/' + room, room=room)

def countdown_thread(room):
    while True:
        current_room = get_room(room)
        if current_room and int(current_room[b"time"]) <= 0:
            break
        socketio.emit('countdown/' + room, current_room, room=room)
        time.sleep(1)
        if current_room:
            updated_time = int(current_room[b"time"]) - 1
            update_room(room, {"time": updated_time})

def reset_countdown(room):
    current_room = get_room(room)
    if current_room:
        update_room(room, {"time": int(current_room[b"timeSet"])})
