# coding=utf-8
from django.shortcuts import render
import sqlite3
import json
from .forms import ConfigForm
from django.http import JsonResponse
from django.http import HttpResponseRedirect

# Create your views here.

def main(request):

    if request.method == 'POST':
        pass

    else:
        pass
    return render(request, 'system/main.html',)

def configed(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    if request.method == 'POST':
        pass

    else:
        sql = " SELECT inputName,ip,description,inputID FROM keys_set"
        cursor.execute(sql)
        form_configed = cursor.fetchall()
    conn.close()
    return render(request, 'system/configed.html',{'form':form_configed})

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
            sql = " SELECT name FROM output_list "
            cursor.execute(sql)
            val = cursor.fetchall()
            conn.close()



        return render(request, 'system/keyconfig.html',{'dict':info_dict,'output_name':val})

    else:
        form = ConfigForm()
        id = request.GET.get('id', default='10000000')
        name = request.GET.get('name', default='10000000')
    return render(request, 'system/config.html',{'name':name,'id':id,'form':form})

def conf_action(request):
    if request.method == 'GET':
        action = request.GET.get('action')
        id = request.GET.get('id')
        if action == 'delete':
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            sql = "DELETE FROM keys_set WHERE inputID = '"+id+"';"
            cursor.execute(sql)
            conn.commit()
            sql = " UPDATE input_select SET free = 1 WHERE dev_ID = '"+id+"'"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return HttpResponseRedirect("configed.html")

def template(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    if request.method == 'POST':
        pass

    else:
        sql = " SELECT * FROM template"
        cursor.execute(sql)
        form_template = cursor.fetchall()
    conn.close()
    return render(request, 'system/template.html',{'form':form_template})

def new_temp(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    if request.method == 'GET':
        sql = " SELECT name FROM output_list "
        cursor.execute(sql)
        val = cursor.fetchall()
        conn.close()

        return render(request, 'system/newtemp.html',{'output_name':val})

def save_temp(request):
    if request.method == 'POST':
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        mes = request.POST['mes']
        status = request.POST['status']
        tem_set = json.loads(mes)
        if status == 'new':
            sql = "INSERT INTO template (name,key1,key2,key3,key4,key5,key6,key7,key8,key9,key10,key11,key12) values('" + tem_set['name']\
                  + "','" + json.dumps(tem_set['key1'], ensure_ascii=False) + "','" + json.dumps(tem_set['key2'], ensure_ascii=False) \
                  + "','" + json.dumps(tem_set['key3'], ensure_ascii=False) + "','" + json.dumps(tem_set['key4'], ensure_ascii=False) \
                  + "','"+json.dumps(tem_set['key5'], ensure_ascii=False)+"','"+json.dumps(tem_set['key6'], ensure_ascii=False)+"','"\
                  +json.dumps(tem_set['key7'], ensure_ascii=False)+"','"+json.dumps(tem_set['key8'], ensure_ascii=False)+"','"\
                  +json.dumps(tem_set['key9'], ensure_ascii=False)+"','"+json.dumps(tem_set['key10'], ensure_ascii=False)+"','"\
                  +json.dumps(tem_set['key11'], ensure_ascii=False)+"','"+json.dumps(tem_set['key12'], ensure_ascii=False)+"')"
            cursor.execute(sql)
            conn.commit()
            conn.close()
        elif status == 'edit':
            sql = "UPDATE template SET key1='" + json.dumps(tem_set['key1'], ensure_ascii=False) + "',key2='"\
                  + json.dumps(tem_set['key2'], ensure_ascii=False) + "',key3='"+ json.dumps(tem_set['key3'], ensure_ascii=False)+"',key4='"\
                  + json.dumps(tem_set['key4'], ensure_ascii=False) +"',key5='"+ json.dumps(tem_set['key5'], ensure_ascii=False) +"',key6='"\
                  + json.dumps(tem_set['key6'], ensure_ascii=False) +"',key7='"+ json.dumps(tem_set['key7'], ensure_ascii=False) +"',key8='"\
                  + json.dumps(tem_set['key8'], ensure_ascii=False) +"',key9='"+ json.dumps(tem_set['key9'], ensure_ascii=False) +"',key10='"\
                  + json.dumps(tem_set['key10'], ensure_ascii=False) +"',key11='"+ json.dumps(tem_set['key11'], ensure_ascii=False) +"',key12='"\
                  + json.dumps(tem_set['key12'], ensure_ascii=False) +"' WHERE name='"+tem_set['name']+"'"
            cursor.execute(sql)
            conn.commit()
            conn.close()

        return JsonResponse({'code': 1, 'msg': 'success'})

def temp_action(request):
    if request.method == 'GET':
        action = request.GET.get('action')
        name = request.GET.get('name')
        if action == 'delete':
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            sql = "DELETE FROM template WHERE name = '"+name+"';"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return HttpResponseRedirect("template.html")
        if action == 'edit':
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            sql = "SELECT * FROM template WHERE name = '"+name+"';"
            cursor.execute(sql)
            val = cursor.fetchone()
            temp_name = val[0]
            key1 = json.loads(val[1])
            key2 = json.loads(val[2])
            key3 = json.loads(val[3])
            key4 = json.loads(val[4])
            key5 = json.loads(val[5])
            key6 = json.loads(val[6])
            key7 = json.loads(val[7])
            key8 = json.loads(val[8])
            key9 = json.loads(val[9])
            key10 = json.loads(val[10])
            key11 = json.loads(val[11])
            key12 = json.loads(val[12])
            sql = " SELECT name FROM output_list "
            cursor.execute(sql)
            form = cursor.fetchall()
            conn.close()
            return render(request, 'system/edittemp.html', {'name':temp_name,'key1':key1,'key2':key2,'key3':key3,
                                                            'key4':key4,'key5':key5,'key6':key6,'key7':key7,'key8':key8,'key9':key9,
                                                            'key10':key10,'key11':key11,'key12':key12,'output_name':form})