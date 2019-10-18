import boto3
from django.contrib.auth.models import User
from FundooApp.models import User_profile
import os

def upload_file(file_name, bucket, object_name):
    # If S3 object_name was not specified, use file_name
    from django.db import IntegrityError
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        if object_name is None:
            raise ValueError
        response = s3_client.upload_fileobj(file_name, bucket, object_name)  # uploading the image to s3
        current_user = User.objects.get(id=int(object_name))  # getting the current user
        user_profile = User_profile.objects.create(profile_pic=str(os.getenv('AMZON_S3_PATH')) + object_name,
                                                   user=current_user)  # getting the path of the file
        user_profile.save()
        return "success"
    except IntegrityError:
        return "success"
    except Exception as e:
        print(e)
        return "fail"
