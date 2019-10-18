#####################################################################################################################
# @author:Muhammed Nisamudheen
# version :{
#               python 3.6
#               django: 2.2
# }
# purpose : Fundoo Application
######################################################################################################################


from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import FundooNotes
from .models import Labels_database
# from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

# from .documents import FundooNotesDocument
# creating a serializer class CreateUserSerializer which uses User Model
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password','first_name','last_name']
        # extra_kwargs = {'email': {'unique': True}}
    #  method to create an database entry in the User model
    def create(self, validated_data):
        user = User(
                email=(validated_data['email']),  # getting the email
                username=validated_data['username'],   # getting the username
                first_name=validated_data['firstname'],   # getting the firstname
                last_name=validated_data['lastname']   # getting the lastname
        )
        if User.objects.filter(email=validated_data['email']).count() > 0:
            return "email present"
        user.is_active=False  # making the isactive field to False
        user.set_password(validated_data['password'])  # setting the password for the user by hashing
        user.save()  # saving the user
        return user

    #  method to activate the user
    def validate(self,id,email):
        result = {
            'success': False,
            'message': 'Something bad happened',
            'data': {}
        }
        try:
            user=User.objects.get(id=id)  # getting the user through the id
            if user.is_active==False:   # checking whether user is active
                user.is_active=True  # making useractive to true for login purposes
                user.save()  # saving the user
                return Response({'message':'UserACTIVATED'})
            else:
                raise ValueError
        except User.DoesnotExist:
            result.message = 'Invalid user'
            return Response(result)
        except ValueError:
            return Response({"message":"not valid"})

    def reset_email_password(self, email, password):
        valide_mail = email['email']  # getting the email of the user
        try:
            user = User.objects.get(email=valide_mail)  # getting the user from the email

            if user.is_active == True:  # checking whether the user is active or not
                user.set_password(password)  # setting the new password for the user
                user.save()  # saving the user
                return Response({'message': 'reset password succesful'})

        except User.DoesNotExist:
            return Response({'message': 'reset password not succesful'})
    # method to reset the password of the user
    # def reset_email_password(self,email,password):
    #     valide_mail=email['email']  # getting the email of the user
    #     try:
    #         user = User.objects.get(email=valide_mail)  # getting the user from the email
    #
    #         if user.is_active==True:  # checking whether the user is active or not
    #             user.set_password(password)  # setting the new password for the user
    #             user.save()  # saving the user
    #             return Response({'message':'reset password succesful'})
    #
    #     except User.DoesNotExist:
    #         return Response({'message': 'reset password not succesful'})

    def get_user(self,email):
        valide_mail = email['email']
        try:
            user = User.objects.get(email=valide_mail)
            return user
        except Exception:
            print("in exception")
            return None

    # def get_useremail(self, id):
    #     valide_id = id['id']
    #     try:
    #         user = User.objects.get(pk=valide_id)
    #         return user
    #     except Exception:
    #         print("in exception")
    #         return None



class NoteSerializer(serializers.ModelSerializer):
    # serializer for serializing the data of the model

    class Meta:
        model=FundooNotes
        fields='__all__'
        # fields=(
        # 'id',
        # 'title' ,
        # 'note' ,
        # 'reminder',
        # 'collaborator',
        # 'color' ,
        # 'image',
        # 'archieve',
        # 'is_trash',
        #
        # )
    #
    # def create(self,**validated_data):
    #
    #     # print(data['title'])
    #     # print(user)
    #     print("inside serializer")
    #     # method for the creation of the notes  with getting the particular user
    #     try:
    #     #
    #     #     notes=FundooNotes(
    #     #         user=user,
    #     #         title=data['title'],
    #     #         note=data['note'],
    #     #         reminder=self.validated_data(data['reminder'),
    #     #         color=data['color'],
    #     #         image=data['image'],
    #     #         archieve=data['archieve'],
    #     #         is_trash=data['trash']
    #     #     )
    #
    #         # notes.save()  # saving the note
    #         FundooNotes(**validated_data)
    #     except Exception as e:
    #        print(e)

    def delete(self,data=None,pk=None):
        if pk is None:
            title=data['title']
            try:
                id=FundooNotes.objects.get(title=title)
                id.delete()
            except TypeError:
                FundooNotes.objects.filter(id=id).delete()

            except Exception as e:
                print(e)
                return Response({'message':'id not present'})
        else:
            try:
                id=FundooNotes.objects.get(id=pk)
                id.delete()
            except Exception as e:
                print(e)
                return  e

    # def get_id(self):
    #     return id


#
# class NotesDocumentSerializer(DocumentSerializer):
#     class Meta:
#         document=FundooNotesDocument
#         fields=(
#             'title',
#             'notes',
#             'reminder',
#
#         )
#
class Label_serializer(serializers.ModelSerializer):
    class meta:
        model=Labels_database
        fields='__all__'
    #
#     # def create(self,data,user,partial=True):
#     #
#     #     label=Labels_database(
#     #         name=name,
#     #         label=NoteSerializer()
#     #
#     #     )
#     #
#     #
#     #
#     #
#     # def get(self,pk):
#     #     try:
#     #         note=FundooNotes.objects.get(pk=pk)
#     #         return Response(note)
#     #     except FundooNotes.DoesNotExist:
#     #         return Response({'message':'value doesnot exist'})
#     #
#     # def update(self,data):
#     #     title=data['title']
#     #     try:
#     #         id=
#     #


