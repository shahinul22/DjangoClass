from django.urls import path
from . import views

urlpatterns = [
    path('', views.des, name='description')  ,
    
]
