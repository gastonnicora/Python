from app.connections.redis import redis_client
import json


def emit_bid(data):
    message = json.dumps({
        data
    })
    redis_client.publish('task_socket_channel', message)

def emit_finish(room):
    message = json.dumps({
        "room":room
    })
    redis_client.publish('task_socket_channel', message)

def emit_updateSesion(data):
    message = json.dumps({
        "data":data
    })
    redis_client.publish('task_socket_channel', message)

def emit_start(room, time):
    message = json.dumps({
        'room':room,
        'time':time
    })
    redis_client.publish('task_socket_channel', message)

def start(room):
    message = json.dumps({
        "room":room
    })
    redis_client.publish('task_socket_channel', message)
