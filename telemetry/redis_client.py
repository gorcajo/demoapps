import os

import redis


redis_host = os.getenv('REDIS_HOST')
redis_port = int(os.getenv('REDIS_PORT'))

client: redis.Redis = None

def instance() -> redis.Redis:
    global client

    if client is None:
        client = redis.Redis(host=redis_host, port=redis_port)

    return client
