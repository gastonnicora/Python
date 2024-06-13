import json
from os import environ
import redis
import jwt
import uuid

from app.helpers.sessions import Sessions

redis_host = environ.get("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379)

class Token:
    _instance = None
    _token= None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            celery={"uuid":str(uuid.uuid4())}
            id,session =Sessions().addSession(celery)
            cls._token=jwt.encode({'uuid':id}, environ.get("SECRET_KEY","1234"), algorithm="HS256")
        return cls._instance
    @classmethod
    def getToken(cls):
        print("secret")
        print(environ.get("SECRET_KEY","1234"))
        return cls._token

def deleteConfirm(uuid):
    message = json.dumps({
        'task_name': "deleteConfirm",
        'uuid': uuid,
        'token':Token().getToken()
    })
    redis_client.publish('task_channel', message)

def finishedArticle(uuid, time):
    message = json.dumps({
        'task_name': "finishedArticle",
        'article': uuid,
        "time": time,
        'token':Token().getToken()
    })
    redis_client.publish('task_channel', message)

def startedArticle(uuid, time):
    message = json.dumps({
        'task_name': "startedArticle",
        'article': uuid,
        "time": time,
        'token':Token().getToken()
    })
    redis_client.publish('task_channel', message)

def startedAuction(uuid, time):
    message = json.dumps({
        'task_name': "startedAuction",
        'article': uuid,
        "time": time,
        'token':Token().getToken()
    })
    redis_client.publish('task_channel', message)

def finisheddAuction(uuid, time):
    message = json.dumps({
        'task_name': "finishedAuction",
        'article': uuid,
        "time": time,
        'token':Token().getToken()
    })
    redis_client.publish('task_channel', message)
