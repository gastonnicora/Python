import json
from os import environ
import redis
import jwt
import uuid

from app.helpers.sessions import Sessions

redis_host = environ.get("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379)


def add_token(token):
    if not redis_client.exists("token"):
        t=str(uuid.uuid4())
        redis_client.hmset("token", t)
        return t
    return get_token()

def get_token():
    return redis_client.hgetall("token")
class Token:
    _instance = None
    _token= None
    def __new__(cls):
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
            celery= get_token()
            celery={"uuid":str(uuid.uuid4())}
            id,session =Sessions().addSession(celery)
            cls._token=jwt.encode({'uuid':id}, environ.get("SECRET_KEY","1234"), algorithm="HS256")
        return cls._instance
    @classmethod
    def getToken(cls):
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

def finishedAuction(uuid, time):
    message = json.dumps({
        'task_name': "finishedAuction",
        'article': uuid,
        "time": time,
        'token':Token().getToken()
    })
    redis_client.publish('task_channel', message)
