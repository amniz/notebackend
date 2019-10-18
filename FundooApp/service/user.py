from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from FundooApp.Serializers import CreateUserSerializer
import jwt
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import os
from FundooApp.Lib.redis import redisoperations
from django.http import HttpResponse
from django.contrib.auth import authenticate

# method to register or signup for the new user with the valid details

def user_register(request):
    print (request.data["username"])
    response = {
        'success':"",
        'data':""
    }
    serializer_object = CreateUserSerializer()  # creating serializer object
    try:
        if request.data["username"] is None:
            raise ValueError("username field required")
        elif request.data["firstname"] is None:
            raise ValueError("firstname field required")
        elif request.data["lastname"] is None:
            raise ValueError("lastname field required")
        elif request.data["email"] is None:
            raise ValueError("email field required")
        elif request.data["password"] is None:
            raise ValueError("password field required")
    except Exception as e :
        response={'data':e,'success':'false'}
        return response
    serializer = CreateUserSerializer.create(serializer_object, validated_data=request.data)  # calling the create
    # method to insert data in the User model
    current_site = get_current_site(request)  # getting the current domain address
    mail_subject = 'Activate your account.'  # subject of the mail
    try:
        payload = {  # payload to be in included in the token
            'email': serializer.email,
            'username': serializer.username,
            'userid': serializer.id

        }
    except Exception:
        response['data']='email already registered'
        response['success']='false'
        return response
    token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')  # generating the token
    message = render_to_string('FundooApp/account_active_email.html', {
        'domain': current_site.domain,
        'token': token,
    })  # generating the message to be send with the email ,rendering the link to account_active_email and giving
    # payload in url
    to_email = serializer.email  # getting the email address
    email = EmailMessage(
        mail_subject, message, to=[to_email]  # creating object of EmailMessage class
    )

    email.send()  # sending the email
    response['data']='Please confirm your email address to complete the registration'
    response['success']='True'
    return response

#activate view key purpose is to activate the user account using the generated token
def user_activate(request, token):
    response = {
        'success': "",
        'data': ""
    }
    payload = jwt.decode(token,'secret')  # decoding the payload from the jwt token
    email = payload['email']  # getting email from the pay load
    userid = payload['userid']  # getting the user id from the payload
    try:
        serializer_object = CreateUserSerializer()  # creating a serializer object
        serializer_object.validate(userid, email)  # calling the validate method in the serializer
        response['data'] = "activation sent"
        response['success'] = 'True'
        return response
    except Exception:
        response['data'] = "Token mismatch"
        response['success'] = 'false'
        return response


# method used for login of the user by providing username and password
def login(request):  # allows the user for login

    response = {
        'success': "",
        'data': ""
    }
    username = request.data['username']  # getting the user name

    password = request.data["password"]  # getting the password

    if username is None or password is None:  # validating whether any of the data is none or not
        response['success']='False'
        response['data']='Please provide both username and password'
        return response

    user = authenticate(username=username, password=password)  # verifying the user name and password

    if not user:
        response['success']='False'
        response['data']='Invalid Credentials'
        return response  # if not found returning

    payload = {
        'id': user.id,
        'username': user.username  # generating payload

    }
    encoded_jwt = jwt.encode(payload, 'secret', algorithm='HS256')  # generating the token
    redis_key = redisoperations()  # creating the redis object
    redis_key.set('token', encoded_jwt)  # setting the redis cache key
    response['success']='True'
    response['data']=encoded_jwt
    return response  # returning the token for the future requirments



# method to send the email by generating token for forgot password
def user_forgot_password(request):

    response = {
        'success': "",
        'data': ""
    }
    try:

        to_email = request.data["email"]  # getting the email from the request

        payload = {
            'email': to_email  # generating the payload
        }

        mail_subject = "forgot password"  # mail subject
        token = jwt.encode(payload, "secret", algorithm='HS256').decode('utf-8')  # generating the token

        message = render_to_string('FundooApp/forgot_password.html', {
            'domain': "localhost:4200",
            "token": token
        })  # redirecting to forgotpassword tempalete and hence reset password
        email = EmailMessage(mail_subject, message, to=[to_email])  # generating the email using EmailMessage class
        email.send()  # sending the email
        response['success']='True'
        response['data']="please do check your email "

        return response
    except Exception as e:
        print(e)
        response['success']='False'
        response['data']=e
        return response

def user_reset(request, token):

    email = jwt.decode(token, 'secret')  # decoding the payload
    password = request.data.get("password")  # getting the new password through the request
    password1 = request.data.get("password1")  # checking whether the password entered by the user are same
    try:
        response = {
            'success': "",
            'data': ""
        }
        if password == password1:
            serializer_object = CreateUserSerializer()  # creating the object of serializer
            serializer_object.reset_email_password(email, password)  # calling reset email method of serializer
            response['success']='True'
            response['data']='password is reset'
            return response
        else:
            raise ValueError("PASSWORDS doesnot match")  # if passwords are not matching raise exception
    except Exception as e:
        response['success']='False'
        response['data']='reset failed'
        return response


def user_logout(request):
    response = {
        'success': "",
        'data': ""
    }
    try:
        redi_obj = redisoperations()
        # redi_obj.remove(request.data.get("username"))
        redi_obj.remove('token')
        response['success']='True'
        response['data']="Succesful"
        return response
    except Exception as e:
        response['success'] = 'False'
        response['data'] = "Unsuccesful"
        return response

