# coding=utf-8
import os
import re
import requests
from django.shortcuts import render
import sqlite3
import json
import hashlib
import STPython

from multikeys import settings
from .forms import ConfigForm
from .forms import UsrForm
from .forms import IpForm
from django.http import JsonResponse
from django.http import HttpResponseRedirect

# Create your views here.

status_dict={}

# conn = sqlite3.connect('db.sqlite3')
database = settings.DATABASES
# conn = sqlite3.connect('db.sqlite3')
conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                        dsn=database['default']['DSN'])
cursor = conn.cursor()
sql = " SELECT inputID,inputName,ip,status FROM keys_set"
cursor.execute(sql)
array = cursor.fetchall()


for i in array:
    i=list(i)
    status_dict[i[0]]=i



def main(request):

    if request.method == 'POST':
        pass

    else:
        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = " SELECT count(*) FROM keys_set"
        cursor.execute(sql)
        num = cursor.fetchone()
        conn.close()

        return render(request, 'system/main.html',{'setnum':num[0],'form':list(status_dict.values())})

def configed(request):
    # conn = sqlite3.connect('db.sqlite3')
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                            dsn=database['default']['DSN'])
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
    # conn = sqlite3.connect('db.sqlite3')
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                            dsn=database['default']['DSN'])
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
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                            dsn=database['default']['DSN'])
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            info_dict = form.cleaned_data
            status = info_dict['status']
            # conn = sqlite3.connect('db.sqlite3')

            cursor = conn.cursor()
            sql = " SELECT name,id FROM output_list "
            cursor.execute(sql)
            output_name = cursor.fetchall()
            sql = " SELECT name FROM template"
            cursor.execute(sql)
            form_template = cursor.fetchall()
            dict_keyname = {'1':info_dict['key1'],'2':info_dict['key2'],'3':info_dict['key3'],'4':info_dict['key4'],
                            '5':info_dict['key5'],'6':info_dict['key6'],'7':info_dict['key7'],'8':info_dict['key8'],
                            '9':info_dict['key9'],'10':info_dict['key10'],'11':info_dict['key11'],'12':info_dict['key12']}
            if status == 'new':
                str = [' ',' ']
                data = json.dumps(str)

                sql = "INSERT INTO keys_set (inputID,inputName,ip,description,keyName,status," \
                      "key1,key2,key3,key4,key5,key6,key7,key8,key9,key10,key11,key12," \
                      "key1id,key2id,key3id,key4id,key5id,key6id,key7id,key8id,key9id,key10id,key11id,key12id) values('"\
                      +info_dict['id']+"','"+info_dict['name']+"','"+info_dict['ip']+"','"+info_dict['description']+"','"+json.dumps(dict_keyname,ensure_ascii=False)+"','off'," \
                      "'"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"" \
                        "','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"','"+data+"')"
                try:
                    cursor.execute(sql)
                except Exception as e:
                    conn.close()
                    return render(request, 'system/config.html',{'name':info_dict['name'],'id':info_dict['id'],'form':form,'status':'new','alter':'error'})
                else:

                    conn.commit()
                    sql = " UPDATE input_select SET free = 0 WHERE dev_ID = '"+info_dict['id']+"'"
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
                    status_dict[info_dict['id']] = [info_dict['id'],info_dict['name'],info_dict['ip'],'off']
                    return render(request, 'system/keyconfig.html',
                                  {'dict': info_dict, 'output_name': output_name, 'form_template': form_template})
            elif status == 'edit':
                sql = "SELECT ip FROM keys_set WHERE inputID='"+info_dict['id']+"'"
                cursor.execute(sql)
                ip_val = cursor.fetchone()
                sql = "UPDATE keys_set SET ip='"+info_dict['ip']+"',description='"+info_dict['description']+"',keyName='"+json.dumps(dict_keyname,ensure_ascii=False)+"' WHERE inputID='"+info_dict['id']+"'"
                try:
                    cursor.execute(sql)
                except Exception as e:
                    conn.close()
                    return render(request, 'system/config.html',{'name':info_dict['name'],'id':info_dict['id'],'form':form,'status':'edit','alter':'error'})
                else:
                    print(status_dict)
                    status_dict[info_dict['id']]= [info_dict['id'],info_dict['name'],info_dict['ip'],'off']


                    conn.commit()
                    sql = "SELECT key1,key2,key3,key4,key5,key6,key7,key8,key9,key10,key11,key12 FROM keys_set WHERE inputID='"+info_dict['id']+"'"
                    cursor.execute(sql)
                    val = cursor.fetchone()
                    key1 = json.loads(val[0])
                    key2 = json.loads(val[1])
                    key3 = json.loads(val[2])
                    key4 = json.loads(val[3])
                    key5 = json.loads(val[4])
                    key6 = json.loads(val[5])
                    key7 = json.loads(val[6])
                    key8 = json.loads(val[7])
                    key9 = json.loads(val[8])
                    key10 = json.loads(val[9])
                    key11 = json.loads(val[10])
                    key12 = json.loads(val[11])
                    conn.close()                        
                    return render(request, 'system/keyconfig.html',
                      {'dict': info_dict, 'output_name': output_name, 'form_template': form_template,'key1':key1,'key2':key2,'key3':key3,
                                                                'key4':key4,'key5':key5,'key6':key6,'key7':key7,'key8':key8,'key9':key9,
                                                                'key10':key10,'key11':key11,'key12':key12})
    else:
        form = ConfigForm()
        id = request.GET.get('id', default='10000000')
        name = request.GET.get('name', default='10000000')
        status = request.GET.get('status', default='10000000')
        if status == 'new':
            return render(request, 'system/config.html',{'name':name,'id':id,'form':form,'status':'new'})
        if status == 'edit':
            # conn = sqlite3.connect('db.sqlite3')
            # conn = STPython.connect('SYSDBA', 'szoscar55')
            cursor = conn.cursor()
            sql = "SELECT inputID,inputName,ip,description,keyName FROM keys_set WHERE inputID = '" + id + "';"
            cursor.execute(sql)
            val = cursor.fetchone()
            val_dict = json.loads(val[4])


            key_dict = {'ip':val[2],'description':val[3],'key1':val_dict['1'],'key2':val_dict['2'],'key3':val_dict['3'],
                        'key4':val_dict['4'],'key5':val_dict['5'],'key6':val_dict['6'],'key7':val_dict['7'],'key8':val_dict['8'],
                        'key9':val_dict['9'],'key10':val_dict['10'],'key11':val_dict['11'],'key12':val_dict['12']}
            form = ConfigForm()
            conn.close()
            return render(request, 'system/config.html', {'name':val[1],'id':val[0],'form': form,'dict':key_dict,'status':'edit'})

def conf_action(request):
    if request.method == 'GET':
        action = request.GET.get('action')
        id = request.GET.get('id')
        if action == 'delete':
            ip = request.GET.get('ip')
            # conn = sqlite3.connect('db.sqlite3')
            conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                    dsn=database['default']['DSN'])
            cursor = conn.cursor()
            sql = "DELETE FROM keys_set WHERE inputID = '"+id+"';"
            cursor.execute(sql)
            conn.commit()
            sql = " UPDATE input_select SET free = 1 WHERE dev_ID = '"+id+"'"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            data = {"method": "update","data":{}}
            try:
                json_data =json.dumps(data)
                r=requests.post('http://'+ip+':8888',data=json_data)
            except Exception as e:
                print(e)
            finally:
                del status_dict[str(id)]
                return HttpResponseRedirect("configed.html")

def template(request):
    # conn = sqlite3.connect('db.sqlite3')
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                            dsn=database['default']['DSN'])
    cursor = conn.cursor()

    if request.method == 'POST':
        pass

    else:
        sql = " SELECT * FROM template"
        cursor.execute(sql)
        form_template = cursor.fetchall()
    conn.close()
    return render(request, 'system/template.html',{'form':form_template})

def saveconf(request):
    # 这里可能有问题
    if request.method == 'POST':
        print(request.POST)
        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
        cursor = conn.cursor()
        mes = request.POST['mes']
        status = request.POST['status']
        key_set = json.loads(mes)

        if status == 'new':
            sql = "UPDATE keys_set SET key1='"+ json.dumps(key_set['key1'], ensure_ascii=False) + "',key2='"\
                  + json.dumps(key_set['key2'], ensure_ascii=False) + "',key3='"+ json.dumps(key_set['key3'], ensure_ascii=False) \
                  +"',key4='"+ json.dumps(key_set['key4'], ensure_ascii=False) +"',key5='"+ json.dumps(key_set['key5'], ensure_ascii=False)\
                  +"',key6='"+ json.dumps(key_set['key6'], ensure_ascii=False) +"',key7='"+ json.dumps(key_set['key7'], ensure_ascii=False) \
                  +"',key8='"+ json.dumps(key_set['key8'], ensure_ascii=False) +"',key9='"+ json.dumps(key_set['key9'], ensure_ascii=False) \
                  +"',key10='"+ json.dumps(key_set['key10'], ensure_ascii=False) +"',key11='"+ json.dumps(key_set['key11'], ensure_ascii=False)\
                  +"',key12='"+ json.dumps(key_set['key12'], ensure_ascii=False) +"',key1id='"+json.dumps(key_set['key1_id'])+"',key2id='"+json.dumps(key_set['key2_id'])\
                  +"',key3id='"+json.dumps(key_set['key3_id'])+"',key4id='"+json.dumps(key_set['key4_id'])+"',key5id='"+json.dumps(key_set['key5_id'])\
                  +"',key6id='"+json.dumps(key_set['key6_id'])+"',key7id='"+json.dumps(key_set['key7_id'])+"',key8id='"+json.dumps(key_set['key8_id'])\
                  +"',key9id='"+json.dumps(key_set['key9_id'])+"',key10id='"+json.dumps(key_set['key10_id'])+"',key11id='"+json.dumps(key_set['key11_id'])\
                  +"',key12id='"+json.dumps(key_set['key12_id'])+"' WHERE inputID ='"+key_set['id']+"'"

            cursor.execute(sql)
            conn.commit()
            sqlip ="SELECT ip FROM keys_set where inputID='"+key_set['id']+"'"
            cursor.execute(sqlip)
            ip = cursor.fetchone()
            conn.close()
            data = {"method": "update", "data": {}}
            try:
                json_data = json.dumps(data)
                r = requests.post('http://'+ip[0]+':8888', data=json_data)
                print(r)
            except Exception as e:
                print(e)

            return JsonResponse({'code': 1, 'msg': 'success'})

def new_temp(request):
    # conn = sqlite3.connect('db.sqlite3')
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                            dsn=database['default']['DSN'])
    cursor = conn.cursor()
    if request.method == 'GET':
        sql = " SELECT name FROM output_list "
        cursor.execute(sql)
        val = cursor.fetchall()
        conn.close()

        return render(request, 'system/newtemp.html',{'output_name':val})

def save_temp(request):
    if request.method == 'POST':

        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
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
            if tem_set['name'] == tem_set['old_name']:
                sql = "UPDATE template SET key1='" + json.dumps(tem_set['key1'], ensure_ascii=False) + "',key2='"\
                  + json.dumps(tem_set['key2'], ensure_ascii=False) + "',key3='"+ json.dumps(tem_set['key3'], ensure_ascii=False)+"',key4='"\
                  + json.dumps(tem_set['key4'], ensure_ascii=False) +"',key5='"+ json.dumps(tem_set['key5'], ensure_ascii=False) +"',key6='"\
                  + json.dumps(tem_set['key6'], ensure_ascii=False) +"',key7='"+ json.dumps(tem_set['key7'], ensure_ascii=False) +"',key8='"\
                  + json.dumps(tem_set['key8'], ensure_ascii=False) +"',key9='"+ json.dumps(tem_set['key9'], ensure_ascii=False) +"',key10='"\
                  + json.dumps(tem_set['key10'], ensure_ascii=False) +"',key11='"+ json.dumps(tem_set['key11'], ensure_ascii=False) +"',key12='"\
                  + json.dumps(tem_set['key12'], ensure_ascii=False) +"' WHERE name='"+tem_set['name']+"'"
            else:
                sql = "UPDATE template SET name='"+tem_set['name']+"',key1='" + json.dumps(tem_set['key1'], ensure_ascii=False) + "',key2='"\
                  + json.dumps(tem_set['key2'], ensure_ascii=False) + "',key3='"+ json.dumps(tem_set['key3'], ensure_ascii=False)+"',key4='"\
                  + json.dumps(tem_set['key4'], ensure_ascii=False) +"',key5='"+ json.dumps(tem_set['key5'], ensure_ascii=False) +"',key6='"\
                  + json.dumps(tem_set['key6'], ensure_ascii=False) +"',key7='"+ json.dumps(tem_set['key7'], ensure_ascii=False) +"',key8='"\
                  + json.dumps(tem_set['key8'], ensure_ascii=False) +"',key9='"+ json.dumps(tem_set['key9'], ensure_ascii=False) +"',key10='"\
                  + json.dumps(tem_set['key10'], ensure_ascii=False) +"',key11='"+ json.dumps(tem_set['key11'], ensure_ascii=False) +"',key12='"\
                  + json.dumps(tem_set['key12'], ensure_ascii=False) +"' WHERE name='"+tem_set['old_name']+"'"
            cursor.execute(sql)
            conn.commit()
            conn.close()

        return JsonResponse({'code': 1, 'msg': 'success'})

def temp_action(request):
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                            dsn=database['default']['DSN'])
    cursor = conn.cursor()
    if request.method == 'GET':
        action = request.GET.get('action')
        name = request.GET.get('name')
        if action == 'delete':


            sql = "DELETE FROM template WHERE name = '"+name+"';"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return HttpResponseRedirect("template.html")
        if action == 'edit':
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

def loadtemp(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = " SELECT * FROM template WHERE name='"+name+"'"
        cursor.execute(sql)
        val = cursor.fetchone()
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
        conn.close()
        return JsonResponse({'key1':key1,'key2':key2,'key3':key3,'key4':key4,'key5':key5,'key6':key6,'key7':key7,
                             'key8':key8,'key9':key9,'key10':key10,'key11':key11,'key12':key12})

def getinfo(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = " SELECT keyName,key1,key2,key3,key4,key5,key6,key7,key8,key9,key10,key11,key12,inputName FROM keys_set WHERE inputID='"+id+"'"
        cursor.execute(sql)
        val = cursor.fetchone()
        keyname = json.loads(val[0])
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
        inputname = val[13]
        conn.close()
        return JsonResponse({'keyname':keyname,'key1':key1,'key2':key2,'key3':key3,'key4':key4,'key5':key5,'key6':key6,'key7':key7,
                             'key8':key8,'key9':key9,'key10':key10,'key11':key11,'key12':key12,'inputname':inputname})


def usr_admin(request):
    # conn = sqlite3.connect('db.sqlite3')
    # cursor = conn.cursor()
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                            dsn=database['default']['DSN'])
    cursor = conn.cursor()
    sql = " SELECT * FROM usradmin "
    cursor.execute(sql)
    val = cursor.fetchall()
    muser = val[0]


    if request.method == 'POST':
        form = UsrForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['usrname']
            password = form.cleaned_data['new_password']
            m = password + "{{sdtzzq}}"
            pw = hashlib.md5(m.encode())
            newpwd = pw.hexdigest()

            # sql = "UPDATE usradmin SET str='"+name+"' WHERE title='usrname'"
            # cursor.execute(sql)
            # conn.commit()
            # sql = "UPDATE usradmin SET str='"+pw.hexdigest()+"' WHERE title='psword'"
            # cursor.execute(sql)
            # conn.commit()
            # conn.close()

            sql = "UPDATE usradmin SET username='{}',passwd='{}' where id={}".format(name,newpwd,muser[0])
            cursor.execute(sql)
            conn.commit()
            return HttpResponseRedirect('/system/usradmin.html')
        else:
            conn.close()
            return render(request, 'system/usradmin.html', {'usrname':muser[1],'form':form,'status':1})
    else:
        conn.close()
        form = UsrForm()


        return render(request, 'system/usradmin.html', {'usrname':muser[1],'form':form,'status':0})


def getconfig(request):
    if request.method == 'POST':
        mes = json.loads(request.POST['MultiK'])
        data = mes['data']
        id = data['id']
        data_ip = data['ip']
        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = " SELECT ip,keyName,key1id,key2id,key3id,key4id,key5id,key6id,key7id" \
              ",key8id,key9id,key10id,key11id,key12id,inputName FROM keys_set WHERE inputID='" + id + "'"
        cursor.execute(sql)
        val = cursor.fetchone()
        if val == None:
            return JsonResponse({'method': 'registe failed', 'data': {'error_code': 404, 'error_reason': 'no id'}})
        else:
            ip = val[0]
            if data_ip == ip:
                keyname = json.loads(val[1])
                m=re.search(r'[0-9]',i[2])
                if m is None:
                    print('ces')
                    return JsonResponse({"method":"registe success"})
                else:
                     return JsonResponse({"method": "registe success", "data": {
                            "preset": [{
                            "channel_in": id,
                            "channel_out": json.loads(val[2]),
                            "preset_name": keyname['1'],
                            "preset_num": "0"
                        }, {
                            "channel_in": id,
                            "channel_out": json.loads(val[3]),
                            "preset_name": keyname['2'],
                            "preset_num": "1"
                        }, {
                            "channel_in": id,
                            "channel_out": json.loads(val[4]),
                            "preset_name": keyname['3'],
                            "preset_num": "2"
                        }, {
                            "channel_in": id,
                            "channel_out": json.loads(val[5]),
                            "preset_name": keyname['4'],
                            "preset_num": "3"
                        }, {
                            "channel_in": id,
                            "channel_out": json.loads(val[6]),
                            "preset_name": keyname['5'],
                            "preset_num": "4"
                        }, {
                            "channel_in": id,
                            "channel_out": json.loads(val[7]),
                            "preset_name": keyname['6'],
                            "preset_num": "5"
                        }, {
                            "channel_in": id,
                            "channel_out": json.loads(val[8]),
                            "preset_name": keyname['7'],
                            "preset_num": "6"
                        }, {
                            "channel_in": id,
                            "channel_out": json.loads(val[9]),
                            "preset_name": keyname['8'],
                            "preset_num": "7"
                        }, {
                            "channel_in": id,
                            "channel_out": json.loads(val[10]),
                            "preset_name": keyname['9'],
                            "preset_num": "8"
                        }, {
                            "channel_in": id,
                            "channel_out": json.loads(val[11]),
                            "preset_name": keyname['10'],
                            "preset_num": "9"
                        }, {
                            "channel_in": id,
                            "channel_out": json.loads(val[12]),
                            "preset_name": keyname['11'],
                            "preset_num": "10"
                       }, {
                            "channel_in": id,
                            "channel_out": json.loads(val[13]),
                            "preset_name": keyname['12'],
                            "preset_num": "11"
                        }]
                    }})
            else:
                return JsonResponse({'method':'registe failed','data':{'error_code' : 405,'error_reason': 'error ip'}})


def config_status(request):
    if request.method == 'POST':
        mes = json.loads(request.POST['MultiK'])
        data = mes['data']
        id = data['id']

    return JsonResponse({'code': 1, 'msg': 'success'})

def get_config_status(request):
    if request.method == 'POST':
        mes = json.loads(request.POST['MultiK'])
        data = mes['data']
        id = data['id']
        ip = data['ip']
    return JsonResponse({'code': 1, 'msg': 'success'})

def check_client(request):
    if request.method == 'POST':
        mes = json.loads(request.POST['MultiK'])
        data = mes['data']
        ip = data['ip']
        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = " SELECT inputID FROM keys_set WHERE ip='"+ip+"'"
        cursor.execute(sql)
        val = cursor.fetchone()
        conn.close()
        if val == None:
            return JsonResponse({'method': 'client query result', 'data': {'right':False, 'id':'none','ip':ip}})
        else:
            return JsonResponse({'method': 'client query result', 'data': {'right':True, 'id':val[0],'ip':ip}})

def connect_status(request):
    if request.method == 'POST':
        mes = json.loads(request.POST['MultiK'])
        data = mes['data']
        method = mes['method']
        ip = data['ip']
        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = " SELECT inputID FROM keys_set WHERE ip='" + ip + "'"
        cursor.execute(sql)
        val = cursor.fetchone()
        if val == None:
            return JsonResponse({'method': 'client query result', 'data': {'right':'false', 'id':'none','ip':ip}})
        else:
            id = val[0]
            conn.close()
            if method == 'client connect':
                print(status_dict)
                status_val = status_dict[str(id)]
                status_val[3] = 'on'
                status_dict[str(id)] = status_val
            elif method == 'client disconnect':
                print(status_dict)
                status_val = status_dict[str(id)]
                status_val[3] = 'off'
                status_dict[str(id)] = status_val
            else:
                return JsonResponse({'code': 1, 'msg': 'error'})
    return JsonResponse({'code': 1, 'msg': 'success'})
# 需要该
def server_status(request):
    # print('0k')
    # return JsonResponse({'code': 1, 'msg': 'success'})
    # conn = sqlite3.connect('db.sqlite3')
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                            dsn=database['default']['DSN'])
    cursor = conn.cursor()
    data_json = {}
    if request.method == 'POST':
        mes = json.loads(request.POST['MultiK'])
        data = mes['data']
        method = mes['method']
        ip = data['ip']
        # print(mes)

        if method == 'server connect':
            sql = "Delete from web_status where id = 1"
            cursor.execute(sql)
            sql = "INSERT INTO web_status(ip,id,status) values ('{}',{},'{}')".format(ip, 1,'on')
            cursor.execute(sql)
            conn.commit()
            conn.close()
            # print('ok')
            return JsonResponse({'code': 1, 'msg': 'success'})
        if method =="server disconnect":
            sql = "Delete from web_status where id = 1"
            cursor.execute(sql)
            sql = "INSERT INTO web_status(ip,id,status) values ('{}',{},'{}')".format(ip, 1, 'off')
            cursor.execute(sql)
            conn.commit()
            conn.close()
            # print('on')
            return JsonResponse({'code': 1, 'msg': 'success'})
        else:
            return JsonResponse({'code': 1, 'msg': 'error'})
    else:
        sql = " SELECT ip,status FROM web_status WHERE id=1"
        cursor.execute(sql)
        array = cursor.fetchall()

        for i in array:
            i = list(i)
            data_json[i[0]] = i
        return JsonResponse({"tcpstatus": list(data_json.values())})




def get_status(request):
    val = list(status_dict.values())
    return JsonResponse({'statusform':val})

'''
这里是具体实现逻辑
'''
def save_ip(request):
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                            dsn=database['default']['DSN'])
    cursor = conn.cursor()
    if request.method == 'POST':
        # conn = sqlite3.connect('db.sqlite3')
        # cursor = conn.cursor()
        ip = request.POST.get("ip")
        port = request.POST.get("description")
        sql = "Delete from web_status where id = 1"
        cursor.execute(sql)
        sql = "INSERT INTO web_status(id,ip,port) values ({},'{}',{})".format(1,ip,port)
        cursor.execute(sql)
        conn.commit()
        dir = os.getcwd()
        file_path = dir + '/configip.ini'
        with open(file=file_path, mode="w", encoding="utf-8") as f:
            f.write(f'[serverinfo]\nip = {ip}\nport = {port}')

        data = {"method": "update server configure", "data" : {"ip":ip,"port":port}}
        json_data =json.dumps(data)
        try:
            r = requests.post("http://0.0.0.0:8080", data=json_data)
        except  Exception as e:
            print('ip端口不存在',e)
        finally:
            return HttpResponseRedirect('/system/createip.html')
        # return JsonResponse({'method': 'registe failed', 'data': {'ip':ip,"port":description}})
    else:
        form = IpForm()
        json_dict = {}
        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = " SELECT ip,status FROM web_status"
        cursor.execute(sql)
        array = cursor.fetchall()
        conn.close()
        for i in array:
            i = list(i)
            json_dict[i[0]] = i
        return render(request, 'system/createip.html', {'form': form,'tcpstatus':list(json_dict.values()),'status': 0})



def tcpstatus(request):
    if request.method =="POST":
        pass
    else:
        json_dict ={}
        # conn = sqlite3.connect('db.sqlite3')
        # conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
        #                         dsn=database['default']['DSN'])
        # cursor = conn.cursor()
        data={"method":"keeplive","data":"ping"}
        json_data = json.dumps(data)
        val =[]
        
        r = requests.post("http://0.0.0.0:8080", data=json_data)
        if r.status_code==200:
            # sql = "UPDATE tcp_status SET status ='on' where id=1"
            # cursor.execute(sql)
            # conn.commit()
            # sql = " SELECT ip,status FROM tcp_status"
            # cursor.execute(sql)
            # array = cursor.fetchall()
            # for i in array:
            #     i = list(i)
            #     json_dict[i[0]] = i
            # conn.close()
            # val = list(json_dict.values())
            # print(val)
            val.append('on')
            return JsonResponse({"tcpstatus":val})
        else:
            print('ip端口不存在')
            val.append('off')
            return JsonResponse({"tcpstatus": val})











