from django.urls import path
from .views import *

urlpatterns = [
    path('login',user_login,name='login'),
    path('register',register,name='register'),
    path('logout',user_logout,name='logout'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/',reset_password_validate,name='reset_password_validate'),
    path('reset_password/',reset_password,name='reset_password'),
    path('dashboard/',dashboard,name='dashboard'),
    path('add-house',add_house,name='add_house')

]