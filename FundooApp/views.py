#####################################################################################################################
# @author:Muhammed Nisamudheen
# version :{
#               python 3.6
#               django: 2.2
# }
# purpose : Fundoo Application
######################################################################################################################
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import jwt
from rest_framework.views import APIView
from . import services
from .Serializers import CreateUserSerializer
import os
from . import utils
# from .services import redisCreate
from dotenv import load_dotenv, find_dotenv
from pathlib import *

load_dotenv(find_dotenv())
env_path = Path('.') / '.env'

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Labels_database
from .models import FundooNotes
from .Serializers import NoteSerializer
import django_redis
# import logging
# import boto3
# from botocore.exceptions import ClientError
from django.contrib.auth.models import User
from .decorators import login_user
# from .models import Labels_database
# from .models import User_profile
from .documents import FundooNotesDocument
from FundooApp.Lib.amazon_s3_files import upload_file
from FundooApp.Lib.amazon_sns import  notification
from FundooApp.service import user,notes

# method to register or signup for the new user with the valid details
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    print("inside register")
    try:
        registration=user.user_register(request)
        if registration['success']==True:
            return Response ({'message':registration},status=HTTP_200_OK)
        else:
            return Response({'message':registration},status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'response':repr(e)},status=HTTP_400_BAD_REQUEST)


# activate view key purpose is to activate the user account using the generated token
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def activate(request, token):
    try:
        response=user.user_activate(request,token)
        if response['success']==True:
            return Response({'message':response},status=HTTP_200_OK)
        else:
            raise Exception
    except Exception :
        return Response({'message':response},status=HTTP_400_BAD_REQUEST)



# method used for login of the user by providing username and password
@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes((AllowAny,))
def login(request):  # allows the user for login

   logged_user = user.login(request)


   try:

       if logged_user['success']=='True':
           return Response({'message',logged_user['data']},status=HTTP_200_OK)
       else:
           raise Exception("login failed")
   except Exception as e:
       print(e)
       return Response({'message',logged_user['data']},status=HTTP_400_BAD_REQUEST)

# @api_view(["GET"])
# def loginsocial(request):
#     return render(request, 'FundooApp/login.html')


def success(request):
    return render(request, 'FundooApp/success.html')


# Create your views here.




# method to send the email by generating token for forgot password
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def forgot_password(request):
    try:
        response=user.user_forgot_password(request)
        if response['success']=='True':
            return Response({'message':response},status=HTTP_200_OK)
        else:
            raise Exception
    except Exception as e:
        return Response({'message':response},status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["GET","POST"])
@permission_classes((AllowAny,))
def resetpassword(request, token):
    print("inside reset")
    response='failed'
    try:
        response=user.user_reset(request,token)
        if response['success']=='True':
            return Response({'message':response},status=HTTP_200_OK)
        else:
            raise Exception("reset failed")
    except Exception as e:
        print("in exception",e)
        return Response({'message':response},status=HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_user
@api_view(["POST"])
def upload(request, *args, user_id=None):

    # for uploading the image in the s3 bucket
    try:

        image = request.FILES.get("image")  # getting the image
        print("inside image image",image)
        response = upload_file(image, 'fundoo-image', str(user_id))  # calling the method for the upload of the file
    except AssertionError as e:
        print("in assertion")
    if response is "success":
        return Response({"message": "success"})
    else:
        return Response({"message": "failed"})

@csrf_exempt
@login_user
@api_view(["GET"])
def getprofilepic(request,user_id):
    response={
        "id":user_id,
        "name":""
    }
    user=User.objects.get(pk=user_id)
    response['name']=user.username
    return Response({'data':response})





@csrf_exempt
@api_view(["GET"])
def logout(request):
    try:
        response=user.user_logout(request)
        if response['success']=='True':
            return Response({"message": response},status=HTTP_200_OK)
        else:
            raise Exception
    except Exception as e:
        return Response({"message": response}, status=HTTP_400_BAD_REQUEST)


#
#
#
#
#
# @login_required
# def home(request):
#     return render(request, 'FundooApp/home.html')
#
#
class Note(APIView):
    #  class to do the crud operations in the database
    # serializer_class = NoteSerializer
    # def get_object(self, pk):
    #     try:
    #         Fundoo_obj = FundooNotes.objects.get(pk=pk)
    #         return Fundoo_obj
    #     except FundooNotes.DoesNotExist:
    #         return Response({'message': 'object Not Found'}, status=HTTP_404_NOT_FOUND)

    @login_user
    def post(self, request, user_id):
        #  posting the notes of the particular user
        try:
            response=notes.note_post(request,user_id)
            if response['success']==True:
                return Response({'message':response},status=HTTP_200_OK)
            else:
                raise Exception
        except Exception:
            return Response({'message':response},status=HTTP_400_BAD_REQUEST)


    @login_user
    def get(self, request,user_id):
        response = notes.get_note(request,user_id)
        print("enthoru",response)
        try:
            if response['success']==True:
                return Response({'message':response},status=HTTP_200_OK)
            else:
                raise Exception
        except Exception:
            return Response({'message':response},status=HTTP_200_OK)

    @login_user
    def delete(self, request, pk=None, user_id=None):
        # function to delete a particular note
        try:
            print("inside del")
            print(request.data)
            print("eyyy",pk)
            response = notes.delete_note(pk, user_id)
            if response['success'] == True:
                return Response({'message': response}, status=HTTP_200_OK)
            else:
                raise Exception
        except Exception:
            return Response({'message': response}, status=HTTP_400_BAD_REQUEST)




    @login_user
    def put(self, request,pk, user_id=None):
        print("inside put")
        response = notes.put_note(request, pk,user_id)
        try:

            if response['success'] == 'True':
                return Response({'message': response}, status=HTTP_200_OK)
            else:
                raise Exception
        except Exception as e:
            print("on final exception of oput")
            print("exception",e)
            return Response({'message': response}, status=HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@login_user
def Archeive(request, user_id):
    print("inside archieve")
    # method to retrieve the archieve notes of the particular person
    try:
        response=notes.archeive_note(user_id)
        if response['success'] == 'True':
            return Response({'message': response}, status=HTTP_200_OK)
        else:
            raise Exception
    except Exception:
        return Response({'message': response}, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@login_user
def trash(request, user_id):
    # method to display the trash notes of the person
    try:
        response = notes.trash_note(user_id)
        if response['success'] == 'True':
            return Response({'message': response}, status=HTTP_200_OK)
        else:
            raise Exception
    except Exception:
        return Response({'message': response}, status=HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@login_user
def reminder(request, user_id):
    print("inside reminder")
    # method to display the reminders set
    try:
        response = notes.reminder(user_id)
        if response['success'] == 'True':
            return Response({'message': response}, status=HTTP_200_OK)
        else:
            raise Exception
    except Exception:
        return Response({'message': response}, status=HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# @login_user
# def get_labels(request, user_id):
#     print("kooi")
#     notes = Labels_database.objects.all()
#     serializer = NoteSerializer(notes, many=True)
#     return Response({'message': serializer.data})
#
#
# # from django.shortcuts import render
#
@api_view(["POST"])
@csrf_exempt
def search(request):
   # method for elastic search temporarly commented for system not become slow
    from elasticsearch_dsl.query import MultiMatch
    print("inside search")
    print(request.data)
    q = request.data['q']
    print(q,"sfestg")
    if q:
        posts = FundooNotesDocument.search().query("match", title=q)

        jsondata=[]
        data={'data':posts}
        for i in data['data']:
            data1 = {}
            print("title",i.title)
            data1['title'] = i.title
            data1['note'] = i.note
            jsondata.append(data1)
            seachdata=tuple(jsondata)
            print(jsondata)
        return Response({'message',seachdata},status=HTTP_200_OK )

    else:
        return Response({'message':'fail'})
#
@api_view(['POST'])
@csrf_exempt
@login_user
def collaborate(request,pk,user_id=None):
    from django.core.exceptions import ObjectDoesNotExist
    from .Exception import SameUser  # creating a custom exception
    note_id=FundooNotes.objects.get(pk=pk)  # getting the note
    try:
        email=request.data['email']  # getting the email to be collaborated
        user=User.objects.get(email=email)  # getting the user of the email
        if user is None:
                raise ObjectDoesNotExist("User does not exist")
        else:
            if user_id == user.id:
                raise SameUser("sorry you can't collaborate yourself")
            note_id.collaborator.add(user)  # adding the user to be collaborated
            return Response({'message':'user added'})
    except Exception as error:
        print("e",error)
        return Response({'message':'caught in exception'+repr(error)})


from rest_framework import viewsets
class Label(APIView):
    # class for doing the CRUD operations on label
    @login_user
    def get(self,request,user_id=None,):
        # method to get all the notes of the uset
        try:
            print("inside my")
            query=Labels_database.objects.filter(user_id=user_id)
            label_set=[]
            for i in query:
                label_set.append(i.name)
            return Response({'message':label_set})
        except Exception as e:
            return Response({'message':repr(e)})

    @login_user
    def post(self,request,user_id=None):
        try:
            Labels_database.objects.create(name=request.data['name'],user_id=user_id)
            return Response({'message':'creation successful'})
        except Exception as e:
            return Response({'message':repr(e)})

    @login_user
    def delete(self,request,user_id=None):
        try:
            label_id=Labels_database.objects.get(pk=request.data['pk'])
            label_id.delete()
            return Response({'message':'delete successful'})
        except Exception as e:
            return Response({'delete unsuccessful':repr(e)})
    @login_user
    def put(self,request,user_id=None):
        try:
            print("inside label put")
            label_id=Labels_database.objects.get(name=request.data['name'])
            print(label_id)
            label_id.name=request.data['newname']
            label_id.save()
            return Response({'message': 'creation successful'})
        except Exception as e:
            return Response({'message': repr(e)})

@api_view(['POST'])
@csrf_exempt
@login_user
def getlabelnotes(request,user_id=None):
    print("request",request)
    print(request.data)
    labelname=request.data['name']
    data=Labels_database.objects.get(name=labelname)
    fundo=FundooNotes.objects.filter(label=data)

    serializer=NoteSerializer(fundo,many=True)
    return Response({"message":serializer.data})

@api_view(['POST'])
@csrf_exempt
@login_user
def getuserdetails(request,user_id=None):
    response = {
        'success': "",
        'owner_user': "",
        'collaborated_users':""

    }
    try:

        print("check", request.data)
        user=User.objects.get(pk=request.data['user'])
        print(user.email)
        print(user)
        # print(type(user))
        # print("namma owner",user[0].data)
        i=0
        ids = request.data.get("collaborated_id")

        emails=[]
        for val in ids:

            usersObj = User.objects.get(pk=val)



            single_email= usersObj.email
            emails.append(single_email)
        response['owner_user']=user.email
        response['collaborated_users']=emails
        return Response({"data":response})
        # for id in request.data['collaborated_id']:
        #
        #     user_set=User.objects.filter(id=id).values()[i]['email']
        #
        #     collaborated_users=user_set
        #     i += 1

            # collaborated_users.append(User.objects.filter(pk=request.data[id]))


        # collaborated_users=User.objects.filter(pk=request.data)
        # owneruser=CreateUserSerializer(user1,many=True)
        #
        # if owner_user:
        #     response["success"]=True
        #     response['owner_user']=user.data[0]['email']
        #     response['collaborated_users']=collaborated_users
        #     return Response (response,status=HTTP_200_OK)
    except Exception as e:
        return Response({"message":e},status=HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@csrf_exempt
@login_user
def delete_collaborator(request,user_id=None):

    email=request.data['email']

    id=request.data['id']

    user=User.objects.get(email=email)

    # dat=FundooNotes.objects.filter(collaborator__id=user.id).filter(id=id[0])
    try:
        FundooNotes.collaborator.through.objects.filter(fundoonotes__id=id[0]).filter(user_id=user.id).delete()
        return Response({"message":"success"})
    except Exception as e:
        return Response({"message": e})



