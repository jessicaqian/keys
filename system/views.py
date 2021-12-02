# coding=utf-8
from django.shortcuts import render
import sqlite3
import json
from .forms import ConfigForm

# Create your views here.



def main(request):

    if request.method == 'POST':
        pass

    else:
        pass
    return render(request, 'system/main.html',)

def configed(request):

    if request.method == 'POST':
        pass

    else:
        pass
    return render(request, 'system/configed.html',)

def free(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    if request.method == 'POST':
        pass

    else:
        sql = " SELECT dev_ID,description FROM input_select WHERE free = 1"
        cursor.execute(sql)
        form_free = cursor.fetchall()
    conn.close()

    return render(request, 'system/free.html',{'form':form_free})

def config(request):

    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            info_dict = form.cleaned_data
            conn = sqlite3.connect('db.sqlite3')
            dict_keyname = {'1':info_dict['key1'],'2':info_dict['key2'],'3':info_dict['key3'],'4':info_dict['key4'],
                            '5':info_dict['key5'],'6':info_dict['key6'],'7':info_dict['key7'],'8':info_dict['key8'],
                            '9':info_dict['key9'],'10':info_dict['key10'],'11':info_dict['key11'],'12':info_dict['key12']}
            cursor = conn.cursor()
            sql = "INSERT INTO keys_set (inputID,inputName,ip,description,keyName) values('"+info_dict['id']+"','"+info_dict['name']+"','"+info_dict['ip']+"','"+info_dict['description']+"','"+json.dumps(dict_keyname,ensure_ascii=False)+"')"

            cursor.execute(sql)
            conn.commit()
            sql = " UPDATE input_select SET free = 0 WHERE dev_ID = '"+info_dict['id']+"'"
            cursor.execute(sql)
            conn.commit()
            conn.close()



        return render(request, 'system/keyconfig.html',{'dict':info_dict})

    else:
        form = ConfigForm()
        id = request.GET.get('id', default='10000000')
        name = request.GET.get('name', default='10000000')
    return render(request, 'system/config.html',{'name':name,'id':id,'form':form})