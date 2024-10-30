import redis
from os import environ


redis_host = environ.get("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379)