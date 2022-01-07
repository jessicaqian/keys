# coding=utf-8
from django.shortcuts import render
import sqlite3
import json
import requests
from .forms import ConfigForm
from django.http import JsonResponse
from django.http import HttpResponseRedirect

# Create your views here.




def main(request):

    if request.method == 'POST':
        pass

    else:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        sql = " SELECT count(*) FROM keys_set"
        cursor.execute(sql)
        num = cursor.fetchone()

        return render(request, 'system/main.html',{'setnum':num[0]})

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
            status = info_dict['status']
            conn = sqlite3.connect('db.sqlite3')
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

                sql = "INSERT INTO keys_set (inputID,inputName,ip,description,keyName) values('"+info_dict['id']+"','"+info_dict['name']+"','"+info_dict['ip']+"','"+info_dict['description']+"','"+json.dumps(dict_keyname,ensure_ascii=False)+"')"

                cursor.execute(sql)
                conn.commit()
                sql = " UPDATE input_select SET free = 0 WHERE dev_ID = '"+info_dict['id']+"'"
                cursor.execute(sql)
                conn.commit()
                conn.close()
                return render(request, 'system/keyconfig.html',
                              {'dict': info_dict, 'output_name': output_name, 'form_template': form_template})
            elif status == 'edit':
                sql = "UPDATE keys_set SET ip='"+info_dict['ip']+"',description='"+info_dict['description']+"',keyName='"+json.dumps(dict_keyname,ensure_ascii=False)+"' WHERE inputID='"+info_dict['id']+"'"
                cursor.execute(sql)
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
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            sql = "SELECT inputID,inputName,ip,description,keyName FROM keys_set WHERE inputID = '" + id + "';"
            cursor.execute(sql)
            val = cursor.fetchone()
            val_dict = json.loads(val[4])


            key_dict = {'ip':val[2],'description':val[3],'key1':val_dict['1'],'key2':val_dict['2'],'key3':val_dict['3'],
                        'key4':val_dict['4'],'key5':val_dict['5'],'key6':val_dict['6'],'key7':val_dict['7'],'key8':val_dict['8'],
                        'key9':val_dict['9'],'key10':val_dict['10'],'key11':val_dict['11'],'key12':val_dict['12']}
            form = ConfigForm()
            return render(request, 'system/config.html', {'name':val[1],'id':val[0],'form': form,'dict':key_dict,'status':'edit'})

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

def saveconf(request):
    if request.method == 'POST':
        print(request.POST)
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        mes = request.POST['mes']
        status = request.POST['status']
        key_set = json.loads(mes)

        if status == 'new':
            sql = "UPDATE keys_set SET key1='"+ json.dumps(key_set['key1'], ensure_ascii=False) + "',key2='"\
                  + json.dumps(key_set['key1'], ensure_ascii=False) + "',key3='"+ json.dumps(key_set['key1'], ensure_ascii=False) \
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
            conn.close()
    return JsonResponse({'code': 1, 'msg': 'success'})






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

def loadtemp(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        conn = sqlite3.connect('db.sqlite3')
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
        conn = sqlite3.connect('db.sqlite3')
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

def getconfig(request):
    if request.method == 'POST':
        mes = json.loads(request.POST['MultiK'])
        data = mes['data']
        id = data['id']
        data_ip = data['ip']
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        sql = " SELECT ip,keyName,key1_id,key2_id,key3_id,key4_id,key5_id,key6_id,key7_id" \
              ",key8_id,key9_id,key10_id,key11_id,key12_id,inputName FROM keys_set WHERE inputID='" + id + "'"
        cursor.execute(sql)
        val = cursor.fetchone()
        if val == None:
            return JsonResponse({'method': 'registe failed', 'data': {'error_code': 404, 'error_reason': 'no id'}})
        else:
            ip = val[0]
            if data_ip == ip:
                keyname = json.loads(val[1])

                return JsonResponse({"method": "registe success", "data": {
                    "preset": [{
                        "channel_in": id,
                        "channel_out": json.loads(val[2]),
                        "preset_name": keyname[0],
                        "preset_num": 0
                    }, {
                        "channel_in": id,
                        "channel_out": json.loads(val[3]),
                        "preset_name": keyname[1],
                        "preset_num": 1
                    }, {
                        "channel_in": id,
                        "channel_out": json.loads(val[4]),
                        "preset_name": keyname[2],
                        "preset_num": 2
                    }, {
                        "channel_in": id,
                        "channel_out": json.loads(val[5]),
                        "preset_name": keyname[3],
                        "preset_num": 3
                    }, {
                        "channel_in": id,
                        "channel_out": json.loads(val[6]),
                        "preset_name": keyname[4],
                        "preset_num": 4
                    }, {
                        "channel_in": id,
                        "channel_out": json.loads(val[7]),
                        "preset_name": keyname[5],
                        "preset_num": 5
                    }, {
                        "channel_in": id,
                        "channel_out": json.loads(val[8]),
                        "preset_name": keyname[6],
                        "preset_num": 6
                    }, {
                        "channel_in": id,
                        "channel_out": json.loads(val[9]),
                        "preset_name": keyname[7],
                        "preset_num": 7
                    }, {
                        "channel_in": id,
                        "channel_out": json.loads(val[10]),
                        "preset_name": keyname[8],
                        "preset_num": 8
                    }, {
                        "channel_in": id,
                        "channel_out": json.loads(val[11]),
                        "preset_name": keyname[9],
                        "preset_num": 9
                    }, {
                        "channel_in": id,
                        "channel_out": json.loads(val[12]),
                        "preset_name": keyname[10],
                        "preset_num": 10
                    }, {
                        "channel_in": id,
                        "channel_out": json.loads(val[13]),
                        "preset_name": keyname[11],
                        "preset_num": 11
                    }]
                }})
            else:
                return JsonResponse({'method':'registe failed','data':{'error_code' : 405,'error_reason': 'error ip'}})







def config_status(request):
    heartbeat()

    return JsonResponse({'code': 1, 'msg': 'success'})

def forward(request):

    return JsonResponse({'code': 1, 'msg': 'success'})
def heartbeat():
    i = 0
    while 1:
        print(1)
        post_data = {'method': 'heartbeat', 'data': 'ping'}
        json_data = json.dumps(post_data)
        try:
            response = requests.post('http://192.168.149.130:8888/index.html', data=json_data)
        except Exception as e:
            i = i+1
            print(i)
            if i>=3:
                return False
        else:
            i=0




