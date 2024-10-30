from app.connections.redis import redis_client
import json


def emit_bid(data):
    message = json.dumps({
        "data":data,
        "task_name":"emit_bid"
    })
    redis_client.publish('task_socket_channel', message)

def emit_finish(room):
    message = json.dumps({
        "room":room,
        "task_name":"emit_finish"
    })
    redis_client.publish('task_socket_channel', message)

def emit_updateSesion(data):
    message = json.dumps({
        "data":data,
        "task_name":"emit_updateSesion"
    })
    redis_client.publish('task_socket_channel', message)

def emit_start(room, time):
    message = json.dumps({
        'room':room,
        'time':time,
        "task_name":"emit_start"
    })
    redis_client.publish('task_socket_channel', message)

def start(room):
    message = json.dumps({
        "room":room,
        "task_name":"start"
    })
    redis_client.publish('task_socket_channel', message)
