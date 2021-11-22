from django.urls import path
from . import views

app_name ='usradmin'

urlpatterns = [
    path('', views.login, name='login'),

]