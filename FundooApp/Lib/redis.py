import redis
import os
try:
    redis_connection = redis.StrictRedis(host='localhost',

                          port=6379,

                          db=0)
except Exception as e:
    print(e)


class redisoperations:
    # method to set the redis key value
    def set(self, key, value):
        try:
            redis_connection.set(key, value)  # setting the key value in redis cache
        except ValueError as e:
            return e
        except KeyError as e:
            return e

    # method to get redis key value
    def get(self, key):
        try:
            data = redis_connection.get(key)  # returning the redis key value
            return data
        except ValueError as e:
            return e
        except KeyError as e:
            return e

    # method to remove the redis token or key
    def remove(self, key):
        try:
            redis_connection.delete(key)  # deleting the key
        except KeyError as e:
            return e
        except ValueError as e:
            return e

    #  method to set hashset values in the redis
    def hset(self, coment, key, value):
        try:
            redis_connection.hset(coment, key, value)
        except Exception:
            return "redis error"

    # method to get all the values in
    def getall(self, para):
        try:
            val = redis_connection.hgetall(para)
            # print("inside val",val)
            return val
        except Exception as e:
            return e

    # method to delete the particular key in redis
    def hdelete(self, name, key):
        try:
            redis_connection.hdel(name, key)
        except Exception:
            return e
