from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('advertisements',advertisements,name='advertisements'),
    path('contact',contact,name='contact')
]