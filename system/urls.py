from django.urls import path
from . import views

app_name ='system'

urlpatterns = [
    path('main.html', views.main),
    path('configed.html', views.configed),
    path('free.html', views.free),

]