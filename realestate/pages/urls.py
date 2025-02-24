from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('advertisements/', advertisements, name='advertisements'),
    path('contact/', contact, name='contact'),
    path('<int:id>/<slug:slug>/', house_detail, name='detail'),
    path('categories/<slug:category_slug>/', category_list, name='category_list'),
    path('profile/<int:id>', profile_show, name='profile_show'),
]