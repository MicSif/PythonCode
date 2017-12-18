import json

class RedisCache:
    def __init__(self,redis_client):
        self._redis = redis_client
    def cache(self,timeout=0):
        def outer(func):
            def inner():
                if timeout==0:
                    return func()
                key=func.__name__
                value = self._redis.get(key)
                if value:
                    return json.loads(value.decode('utf-8'))
                else:
                    msg=func()
                    self._redis.setex(key,json.dumps(msg),timeout)
                    return msg
            return inner
        return outer


