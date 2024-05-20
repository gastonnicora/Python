import json
import os
import redis

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379)

def deleteConfirm(uuid):
    message = json.dumps({
        'task_name': "deleteConfirm",
        'uuid': uuid
    })
    redis_client.publish('task_channel', message)

def finishedArticle(uuid, time):
    message = json.dumps({
        'task_name': "finishedArticle",
        'article': uuid,
        "time": time
    })
    redis_client.publish('task_channel', message)

def startedArticle(uuid, time):
    message = json.dumps({
        'task_name': "startedArticle",
        'article': uuid,
        "time": time
    })
    redis_client.publish('task_channel', message)

def startedAuction(uuid, time):
    message = json.dumps({
        'task_name': "startedAuction",
        'article': uuid,
        "time": time
    })
    redis_client.publish('task_channel', message)
