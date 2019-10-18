from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=  models.CASCADE)

    age=models.IntegerField()
    def __str__(self):
        return self.user.username


class Labels_database(models.Model):
    name=models.CharField(max_length=255,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FundooNotes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    title=models.CharField(max_length=255,blank=True,null=True)
    note=models.TextField(max_length=1025,null=True,blank=True)
    reminder=models.DateTimeField(default=datetime.now(),blank=True,null=True)
    collaborator=models.ManyToManyField(User,null=True,blank=True,related_name='collaborator')
    color=models.CharField(max_length=10,default='#FFFFFF',blank=True)
    image=models.TextField(default='default',blank=True)
    archieve=models.BooleanField(default=False,blank=True)
    is_trash=models.BooleanField(default=False,blank=True)
    label=models.ManyToManyField(Labels_database,null=True,blank=True,related_name='label')
    createdAt=models.DateTimeField(default=datetime.now(),null=False, blank=True)
    modifiedAt=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.title


class User_profile(models.Model):
    profile_pic=models.URLField(max_length=300,blank=True,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name






# from django.contrib.auth.models import AbstractUser
# class User(AbstractUser):
#     name = models.CharField(max_length=100, blank=True, null=True)




# class Creation_Details(FundooNotes,Labels):


