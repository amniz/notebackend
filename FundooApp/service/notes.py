from django.contrib.auth.models import User
from FundooApp.Serializers import NoteSerializer
from FundooApp.models import FundooNotes
from FundooApp.Lib.redis import redisoperations
from datetime import datetime
from FundooApp.Lib.amazon_sns import notification
def collaborate(request,pk,user_id):
    from django.core.exceptions import ObjectDoesNotExist
    from FundooApp.Exception import SameUser  # creating a custom exception
    note_id=FundooNotes.objects.get(pk=pk)  # getting the note
    response={
        'success': "",
        'data': ""
    }
    try:
        user=user_id
        if user is None:
                raise ObjectDoesNotExist("User does not exist")
        else:
            if user_id == user.id:
                raise SameUser("sorry you can't collaborate yourself")
            note_id.collaborator.add(user)  # adding the user to be collaborated
            response['success']='True'
            response['data']='user added'
            return response
    except Exception as error:
        response['success']='False'
        response['data']='caught in exception'+repr(error)


def note_post(request, user_id):
    #  posting the notes of the particular user
    print("hello",request.data)
    request.data1 = request.data.copy()
    try:
        response = {
            'success': "",
            'data': ""
        }
        if 'collaborator' in request.data and 'collaborator'!="":

            email = request.data['collaborator']
            user = User.objects.get(email=email)
            request.data1['collaborator']=user.id



        Fundoo_user = User.objects.get(id=user_id)  # getting the user from the database


        c={'user':Fundoo_user.id}
        # c.update(request.data)

        request.data1.update(c)
        # request.data['user']=Fundoo_user
        serializer = NoteSerializer(data=request.data1)
        if serializer.is_valid(raise_exception=True):
            note_saved = serializer.save()
        # validated_data=request.data
        # validated_data.user=Fundoo_user
        # serializer1 = NoteSerializer(partial=True)  # creating the serializer object
        # print("dret",serializer1)
        #
        # serializer1.create(**validated_data)  # creating the serializer


        # data = FundooNotes.objects.all().filter(user_id=user_id)  # getting the data according to the user id
        # serializer = NoteSerializer(data, many=True)  # creating serializer object with the specified data
        # # token_object = redisoperations()  # creating the object of the redis cache
        # # token_object.hset("funddoonotes", "funddonotes",
        # #                   str(serializer.data))  # creating hashset for the redis caching
        response['success']='True'
        response['data']='success'
        return response
    except Exception as e:
        print(e)
        response['success'] = 'False in initial'
        response['data'] = 'failed'
        return response

def get_note(request, user_id):
    # method or getting the notes of the particular user
    print("inside initial note get")

    try:
        response = {
            'success': "",
            'data': "",
            'collaboratednotes':""
        }
        if user_id is not None:
            data = FundooNotes.objects.all().filter(user_id=user_id).filter(archieve=False).filter(
            is_trash=False).order_by('createdAt') # getting the data of the particular user
            serializer = NoteSerializer(data, many=True)  # creating a serializer

            response['success'] = 'True'
            response['data'] = serializer.data

            user = User.objects.get(id=user_id)
            note = user.collaborator.all()  # getting the collaborated notes
            serializer1=NoteSerializer(note,many=True)
            response2=serializer1.data
            response['collaboratednotes']=response2
            return response
        else:
            raise ValueError('user not found')
    except Exception as e:
        print("inside initial not get exception",e)
        response['success'] = 'False'
        response['data'] = repr(e)
        return response

def delete_note(pk=None, user_id=None):
    # function to delete a particular note
    response = {
        'success': "",
        'data': ""
    }



    try:
        Fundoo_object = FundooNotes.objects.get(id=pk)
        if Fundoo_object.user_id == user_id:
            id = FundooNotes.objects.get(id=pk)
            id.delete()
            response['success'] = 'True'
            response['data'] = 'delete successful'
            return response
        else:
            response['success'] = 'False'
            response['data'] = 'delete unsuccessful user not authorized'
            return response
    except FundooNotes.DoesNotExist:
        response['success'] = 'False'
        response['data'] = 'value doesnot found'
        return response
    except Exception as e:
        response['success'] = 'False'
        response['data'] = repr(e)
        return response




def put_note(validated_data,instance1,user_id=None):
    print("validated data",validated_data)
    print("valideated dats data",validated_data.data)
    validated_data1 = validated_data.data.copy()
    print(user_id)
    user=User.objects.filter(id=user_id).values()
    print("userrr",user[0]['email'])
    email=user[0]['email']
    print("dfdsgfs",email)
    if 'collaborator' in validated_data.data:
        try:
            email=validated_data.data['collaborator']
            user=User.objects.get(email=email)
            print("user",user)

            collaborate(validated_data,instance1,user)
            print("hai")
            validated_data1['collaborator'] = [user.id]
            print("hello")
        except Exception as e:
            print("exception on that",e)
    try:
        response={
            'success':"",
            'data':""
        }
        print("hai ourtside if")
        if 'reminder' in validated_data.data:
            print("hello inside if")
            newreminder=notification()
            newreminder.create_topic("first","second",email_addr=email)
            print("created")

        print("hai2")
        instance=FundooNotes.objects.get(pk=instance1)
        print("hello2")
        serializer = NoteSerializer(
            instance=instance,
            data=validated_data1,
            partial=True
        )
        print("hello 3")
        print(serializer.initial_data)
        serializer.is_valid(raise_exception=False)
        print("hello 4")
        serializer.save()
        print("after save")
        # data=validated_data
        # print("hai")
        # serializer=NoteSerializer(data,partial=True)
        # print("hello")
        # serializer.update()
        # print("kooi")
        response['success']='True'
        response['data']=validated_data.data
        return response
    except Exception as e:
        print('exception here',e)
        return  repr(e)
#
# def put_note(request, pk, user_id=None):
#     try:
#         note_object = FundooNotes.objects.get(id=pk)  # getting the object using the primary key
#         if note_object.user_id == user_id:
#             if request.data.get('title') is not None:
#                 try:
#                     note_object.title = request.data.get('title')  # setting the title value
#                 except Exception as e:
#                     return repr(e)
#             if request.data.get('note') is not None:
#                 try:
#                     note_object.note = request.data.get('note')
#                 except Exception as e:
#                     return repr(e)
#             if request.data.get('reminder') is not None:
#                 try:
#                     note_object.reminder = request.data.get('reminder')
#                 except Exception as e:
#                     return repr(e)
#             if request.data.get('collaborator') is not None:
#                 try:
#                     note_object = request.data.get('collaborator')
#
#                     collaborate(note_object, pk, user_id)
#                 except Exception as e:
#                     return repr(e)
#             if request.data.get('color') is not None:
#                 try:
#                     note_object.color = request.data.get('color')
#                 except Exception as e:
#                     return repr(e)
#             if request.data.get('image') is not None:
#                 try:
#                     note_object.image = request.data.get('image')
#                 except Exception as e:
#                     return repr(e)
#             if request.data.get('archieve') is not None:
#                 try:
#                     note_object.archieve = request.data.get('archieve')
#                 except Exception as e:
#                     return repr(e)
#             if request.data.get('trash') is not None:
#                 try:
#                     note_object.is_trash = request.data.get('trash')
#                 except Exception as e:
#                     return repr(e)
#             note_object.modifiedAt=datetime.now()
#             note_object.save()  # saving the object
#             return "success"
#         else:
#             raise ValueError
#     except Exception as e:
#         return repr(e)

def archeive_note(user_id):
    # method to retrieve the archieve notes of the particular person
    try:
        response = {
            'success': "",
            'data': ""
        }
        data = FundooNotes.objects.filter(user_id=user_id).filter(archieve=True).exclude(is_trash=True)
        print(data)
        serializer = NoteSerializer(data, many=True)
        response['success'] = 'True'
        response['data'] = serializer.data
        return response
    except Exception as e:
        print('exception', e)
        response['success'] = 'False'
        response['data'] = serializer.data
        return response


def trash_note(user_id):
    # method to display the trash notes of the person
    try:
        response = {
            'success': "",
            'data': ""
        }
        notes = FundooNotes.objects.filter(user_id=user_id).filter(is_trash=True)
        serializer = NoteSerializer(notes, many=True)
        response['success'] = 'True'
        response['data'] = serializer.data
        return response
    except Exception as e:
        print('exception', e)
        response['success'] = 'False'
        response['data'] = serializer.data
        return response

def reminder(user_id):
    print("inside reminder")
    # method to display the reminders set
    try:
        response = {
            'success': "",
            'data': ""
        }

        notes = FundooNotes.objects.filter(user_id=user_id).exclude(reminder='2019-05-20 10:30:00+00')

        serializer = NoteSerializer(notes, many=True)

        response['success']='True'
        response['data']= serializer.data
        return response
    except Exception as e:
        print('exception',e)
        response['success'] = 'False'
        response['data'] = serializer.data
        return response




