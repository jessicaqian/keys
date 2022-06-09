from django.urls import path
from . import views

app_name ='usradmin'

urlpatterns = [
    path('', views.login, name='login'),
    path('devices', views.devices),
    path('snmp_key', views.snmp_key)
]