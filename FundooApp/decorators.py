from FundooApp.Lib.redis import redisoperations
import jwt
import os
from .models import User


def login_user(original_function):
    # function to authenticate the login user
    def wrapper(*args, **kwargs):
        redis_object = redisoperations()
        jwt_token = redis_object.get('token')
        decoded_token = jwt.decode(jwt_token, 'secret')
        user_id = decoded_token['id']
        id = User.objects.values('id')
        for i in range(len(id)):
            if (id[i]['id']) == user_id:  # getting the user id from the query set
                return original_function(*args, **kwargs,user_id=user_id)
                break
            else:
                continue

    return wrapper


