from django.urls import path,include
from . import views
from django.urls import re_path
from rest_framework_swagger.views import get_swagger_view
from . import router
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("",views.Label,base_name='labels')

# schema_view = get_swagger_view(title='Pastebin API')
urlpatterns=[
     path('',views.login, name='login'),
    # path('home',views.home),
    # # path('apidoc',schema_view),
    path('forgot',views.forgot_password,name='forgot'),
    path('activate/<token>/',views.activate, name='activate'),
     path('resetpassword/<token>/',views.resetpassword, name='resetpassword'),
     path('register',views.register,name='register'),
    path('logout',views.logout,name="logout"),
    path('upload',views.upload,name="upload"),
    path('getprofilepic',views.getprofilepic,name="getprofilepic"),
    # path('upload',views.upload),
    # path(r'^oauth/', include('social_django.urls', namespace='social')),
    # path('loginsocial',views.loginsocial,name='loginsocial'),
    # path('success',views.success),
    path('Note',views.Note.as_view()),
    path('Note/<int:pk>',views.Note.as_view()),
    path('archieve',views.Archeive,name='archieve'),
    path('search',views.search,name='search'),
    path('collaborate/<int:pk>',views.collaborate,name='collaborate'),
    # path('reminder',views.Reminder,name='reminder'),
    path('trash',views.trash,name='trash'),
    path('reminder',views.reminder,name='reminder'),
    # path('labels',views.get_labels,name='labels'),
    path('labels',views.Label.as_view()),
    path('getlabel',views.getlabelnotes,name='getlabelnotes'),
    path('userdetails',views.getuserdetails,name='userdetails'),
    path('deletecollaborator',views.delete_collaborator,name='deletecollaborator')
    # # path('route',router)
    # # path('demo', views.demo, name='demo')
    #
    # # path('activate/',views.activate,name='activate')
    # # path('activate/(?P<token>[0-9A-Za-z]{1,1000}.[0-9A-Za-z]{1,1000}.[0-9A-Za-z]{1,1000})/$',views.activate,name='activate')
]
