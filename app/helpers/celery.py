import json
import os
import redis
import jwt
import uuid

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379)
token = jwt.encode({'uuid':str(uuid.uuid4)}, os.environ.get("SECRET_KEY","1234"), algorithm="HS256")


def deleteConfirm(uuid):
    message = json.dumps({
        'task_name': "deleteConfirm",
        'uuid': uuid,
        'token':token
    })
    redis_client.publish('task_channel', message)

def finishedArticle(uuid, time):
    message = json.dumps({
        'task_name': "finishedArticle",
        'article': uuid,
        "time": time,
        'token':token
    })
    redis_client.publish('task_channel', message)

def startedArticle(uuid, time):
    message = json.dumps({
        'task_name': "startedArticle",
        'article': uuid,
        "time": time,
        'token':token
    })
    redis_client.publish('task_channel', message)

def startedAuction(uuid, time):
    message = json.dumps({
        'task_name': "startedAuction",
        'article': uuid,
        "time": time,
        'token':token
    })
    redis_client.publish('task_channel', message)

def finisheddAuction(uuid, time):
    message = json.dumps({
        'task_name': "finishedAuction",
        'article': uuid,
        "time": time,
        'token':token
    })
    redis_client.publish('task_channel', message)
