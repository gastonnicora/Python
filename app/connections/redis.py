import redis
from os import environ


redis_host = environ.get("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379)

def acquire_lock(lock_name,seconds):
    return redis_client.set(lock_name, "1", nx=True, ex=seconds) 

def release_lock(lock_name):
    redis_client.delete(lock_name)