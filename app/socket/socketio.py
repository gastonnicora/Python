from flask_socketio import SocketIO
from flask import request
from flask_socketio import emit, join_room, leave_room
import time
from threading import Thread
import logging

# Configuración del logger
logging.basicConfig(level=logging.DEBUG,  # Cambia a INFO o ERROR según lo necesites
                    format='%(asctime)s - %(levelname)s - %(message)s')


socketio = SocketIO(cors_allowed_origins='*', async_mode='gevent', ping_timeout=180, ping_interval=30, logger=True, engineio_logger=True)


users={}
rooms={}


@socketio.on('connect')
def test_connect():
    print("coneccion")
    emit('connect', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print("desconeccion")
    if users[request.sid] and users[request.sid]["room"]:
        room = users[request.sid]["room"]
        rooms[room]["users"].remove(users[request.sid])
        leave_room(room, request.sid)
        emit('joinToRoom/' + room, rooms[room], room=room)
        users.pop(request.sid,None)

@socketio.on_error()
def error_handler(e):
    event_name = request.event if hasattr(request, 'event') else 'unknown event'
    error_message = str(e)
    
    logging.error(f"Error en la conexión {request.sid} en el evento '{event_name}': {error_message}")
    logging.error(f"Headers: {dict(request.headers)}")  # Detalles adicionales sobre la solicitud



@socketio.on_error_default
def default_error_handler(e):
    print(f'Default error: {e}')

@socketio.on('borrarUser')
def disconnect(data):
    print("borrar user")
    users.pop(request.sid, None)

@socketio.on('coneccion')
def test_coneccion(data):
    try:
        print("user coneccion")
        if data:
            users[request.sid]= data
            print("coneccion data:")
            print(data)
            join_room(data["uuid"], request.sid)
    except Exception as e:
        error_handler(e) 
    


@socketio.on('join')
def on_join(data):
    try:
        print("join")
        room = data['room']
        join_room(room, request.sid)
        if room not in rooms:
            rooms[room] = {"users": [], "time": 0, "timeSet": 0, "bool": False}
        if request.sid in users:
            users[request.sid]["room"]=room
            rooms[room]["users"].append(users[request.sid])
            emit('joinToRoom/' + room, rooms[room], room=room)
    except Exception as e:
        error_handler(e) 
    

@socketio.on('leave')
def on_leave(data):
    print("leave")
    room = data['room']
    if room in rooms and request.sid in users:
        users[request.sid]["room"]=None
        rooms[room]["users"].remove(users[request.sid])
    else:
        print("La sala especificada no existe.")
    leave_room(room, request.sid)
    emit('joinToRoom/' + room, rooms[room], room=room)

def emit_bid(data):
    print("emit bid")
    room = data['room']
    if room in rooms and rooms[room].get("time") and rooms[room].get("time") >= 0:
        reset_countdown(room)
    socketio.emit('bidRoom/' + room, data["bid"], room=room)  

def emit_finish(room):
    print("emit finish")
    socketio.emit('finishRoom/' + room, {'data': "finish"}, room=room)

@socketio.on('leave_session')
def on_leave_session(data):
    print("leave")
    leave_room(data["uuid"], request.sid)

def emit_updateSesion(data):
    print("update session")
    socketio.emit('updateSession', {'data': data}, room=data["uuid"])

def emit_start(room, time):
    print("emit start")
    if room not in rooms:
        rooms[room] = {"users": [], "time": int(time), "timeSet": int(time), "bool": False}
    if not rooms[room].get("bool"):
        rooms[room]["time"] = int(time)
        rooms[room]["timeSet"] = int(time)
        rooms[room]["bool"] = True
        thread = Thread(target=countdown_thread, args=(room,))
        thread.start()
    socketio.emit('startRoom/' + room, room=room)

def start(room):
    print("start")
    if room not in rooms:
        rooms[room] = {"users": []}
    socketio.emit('startRoom/' + room, room=room)

def countdown_thread(room):
    while True:
        if room not in rooms or rooms[room]["time"] <= 0:
            break
        socketio.emit('countdown/' + room, rooms[room], room=room)
        rooms[room]["time"] -= 1
        time.sleep(1)

def reset_countdown(room):
    if room in rooms:
        rooms[room]["time"] = rooms[room]["timeSet"]
