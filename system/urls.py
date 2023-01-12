from django.urls import path
from . import views

app_name = 'system'

urlpatterns = [
    path('main.html', views.main),
    path('free.html', views.free),
    path('config.html', views.config),
    path('configed.html', views.configed),
    path('template.html', views.template),
    path('newtemp.html', views.new_temp),
    path('task.html', views.task),
    path('task_edit.html', views.task_edit),
    path('usradmin.html', views.usr_admin),
    path('createip.html', views.save_ip),

    path('configedaction', views.conf_action),
    path('saveTemplate', views.save_temp),
    path('deployTemplate', views.deploy_temp),
    path('deleteTemplate', views.delete_temp),
    path('tempAction', views.temp_action),
    path('loadtemp', views.loadtemp),
    path('getTempDetail', views.get_temp_detail),
    path('saveTask', views.task_save),
    path('deleteTask', views.task_delete),
    path('deployTask', views.task_deploy),
    path('saveconf', views.saveconf),
    path('getinfo', views.getinfo),
    path('getconfig', views.getconfig),
    path('configStatus', views.config_status),
    path('checkClient', views.check_client),
    path('connectStatus', views.connect_status),
    path('serverStatus', views.server_status),
    path('getStatus', views.get_status),
    path('getServerUsage', views.getServerUsage),
    path('tcpStatus', views.tcpstatus),
    path('devices', views.devices),
    path('ipConflict', views.ip_conflict),
    path('consumeMsg', views.consume_msg),
    path('logDownload', views.log_download),
]