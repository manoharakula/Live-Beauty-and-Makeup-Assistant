from django.urls import path
from virtual import views
from virtual.views import PostJsonView


urlpatterns = [
    path('', views.virtual_demo, name='virtual'),
    path('lips/',views.lips , name= "lips") ,
    path('subclass/<str:class>/<str:name>' , PostJsonView.as_view() , name = "subclass" ),
    path('myprofile/<int:objectid>', views.profile , name = "profile") 
]

#  path('myprofile/(?P<objectname>\w+)', views.profile , name = "profile") 
