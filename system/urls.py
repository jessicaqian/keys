from django.urls import path
from . import views

app_name ='system'

urlpatterns = [
    path('main.html', views.main),
    path('configed.html', views.configed),
    path('free.html', views.free),
    path('config.html',views.config),
    path('template.html',views.template),
    path('configedaction',views.conf_action),
    path('newtemp.html',views.new_temp),
    path('saveTemplate',views.save_temp),
    path('tempAction',views.temp_action),
    path('loadtemp',views.loadtemp),
    path('saveconf',views.saveconf),
    path('getinfo',views.getinfo),
    path('getconfig',views.getconfig),
    path('configStatus',views.config_status),
    path('forward',views.forward),
    path('usradmin.html',views.usr_admin),
    path('reforward',views.re_forward)

]