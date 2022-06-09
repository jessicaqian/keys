import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import NameForm
import STPython
from multikeys import settings
database = settings.DATABASES
# Create your views here.

def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            return HttpResponseRedirect('/system/main.html')
        else:
            return render(request, 'usradmin/login.html', {'form': form})
    else:
        form = NameForm()
    return render(request, 'usradmin/login.html', {'form': form})


def devices(request):
    if request.method =="POST":
        pass
    else:

        json_data = []
        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
        cursor = conn.cursor()

        sql = " SELECT inputID,inputName,description,ip,status FROM keys_set"
        cursor.execute(sql)
        array = cursor.fetchall()
        for i in array:
            json_data.append({
                "id":i[0],
                "name":i[1],
                "description":i[2],
                "ip":i[3],
                "status":i[4]+'line'
            })
        return HttpResponse(json.dumps(json_data))

def snmp_key(request):
    if request.method =="POST":
        pass
    else:

        json_data = []
        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
        cursor = conn.cursor()

        sql = " SELECT inputID,inputName,description,ip,status FROM keys_set"
        cursor.execute(sql)
        array = cursor.fetchall()
        for i in array:
            json_data.append({
                "id":i[0],
                "name":i[1],
                "description":i[2],
                "status":i[4]+'line'
            })
        return HttpResponse(json.dumps(json_data))
