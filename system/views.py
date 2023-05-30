# coding=utf-8
import os
import re
import psutil
import requests
import json
import hashlib
import sqlite3
import STPython
import logging
import queue

from multikeys import settings
from .forms import ConfigForm
from .forms import UsrForm
from .forms import IpForm
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.http import FileResponse
from django.http import HttpResponseRedirect

# Create your views here.
msgQueue = queue.Queue(0)
database = settings.DATABASES
http_timeout = 2  #与终端的HTTP连接超时时间

status_dict = {}

#创建数据库
conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
cursor = conn.cursor()

sql = "SELECT RELNAME FROM sys_class WHERE RELKIND='r'"
cursor.execute(sql)
array = cursor.fetchall()
tabel1 = ('USRADMIN',)
tabel2 = ('INPUT_SELECT',)
tabel3 = ('OUTPUT_LIST',)
tabel4 = ('KEYS_SET',)
tabel5 = ('TEMPLATE',)
tabel6 = ('TASK',)
tabel7 = ('WEB_STATUS',)

#判断USRADMIN是否存在，如果不存在创建
if tabel1 in array:
    pass
else:
    cursor.execute('create table usradmin (id integer PRIMARY KEY AUTO_INCREMENT,username text,passwd text)')
    conn.commit()
    cursor.execute('INSERT INTO usradmin (username,passwd)values (:a,:b)', ('admin', '4c635087df1041bd13681ee3c6eb04d5'))
    conn.commit()
    print('USRADMIN表创建成功')

#判断INPUT_SELECT是否存在，如果不存在创建
if tabel2 in array:
    pass
else:
    cursor.execute('create table input_select (dev_ID integer, description text, free integer)')
    conn.commit()
    rows = [(1, '测试输入1', 1), (2, '测试输入2', 1), (3, '测试输入3', 1)]
    sql = "insert into input_select (dev_id,description,free) values (:a,:b,:o)"
    cursor.executemany(sql, rows)
    conn.commit()
    print('INPUT_SELECT表创建成功')

#判断OUTPUT_LIST是否存在，如果不存在创建
if tabel3 in array:
    pass
else:
    cursor.execute('create table output_list (id integer PRIMARY KEY, name text)')
    conn.commit()
    rows = [(1, '测试输出1'), (2, '测试输出2'), (3, '测试输出3')]
    sql = 'insert into output_list (id,name) values (:a,:b)'
    cursor.executemany(sql, rows)
    conn.commit()
    print('OUTPUT_LIST表创建成功')

#判断KEYS_SET是否存在，如果不存在创建
if tabel4 in array:
    pass
else:
    sql = "create table keys_set (id integer PRIMARY KEY AUTO_INCREMENT,inputID text ,inputName text,ip text,description text,keyName varchar (1000),key1 varchar (200),key2 varchar(200),key3 varchar(200),key4 varchar(200),key5 varchar(200),key6 varchar(200),key7 varchar(200),key8 varchar(200),key9 varchar(200),key10 varchar(200),key11 varchar(200),key12 varchar(200),key1id varchar (200),key2id varchar(200),key3id varchar(200),key4id varchar(200),key5id varchar(200),key6id varchar(200),key7id varchar(200),key8id varchar(200),key9id varchar(200),key10id varchar(200),key11id varchar(200),key12id varchar(200),status text)"
    cursor.execute(sql)
    conn.commit()
    print('KEYS_SET表创建成功')

# 判断TEMPLATE是否存在，如果不存在创建
if tabel5 in array:
    pass
else:
    sql = "create table template (name text,key1 varchar (200),key2 varchar(200),key3 varchar(200),key4 varchar(200),key5 varchar(200),key6 varchar(200),key7 varchar(200),key8 varchar(200),key9 varchar(200),key10 varchar(200),key11 varchar(200),key12 varchar(200),keyName varchar (1000))"
    cursor.execute(sql)
    conn.commit()
    print('TEMPLATE表创建成功')

# 判断TASK是否存在，如果不存在创建
if tabel6 in array:
    pass
else:

    sql = "create table task (name text ,taskmap varchar (1000))"
    cursor.execute(sql)
    conn.commit()
    print('TASK表创建成功')


# 判断WEB_STATUS是否存在，如果不存在创建
if tabel7 in array:
    pass
else:
    cursor.execute('create table web_status (id integer PRIMARY KEY AUTO_INCREMENT,ip text ,status text,port text)')
    conn.commit()
    print('WEB_STATUS表创建成功')


sql = " SELECT inputID,inputName,ip,status FROM keys_set"
cursor.execute(sql)
array = cursor.fetchall()
for i in array:
    i = list(i)
    status_dict[i[0]] = i

# 用户操作logger配置
userlogger = logging.getLogger("MULTIKEYS_SERVER_USER")
userlogger.setLevel(logging.INFO)
userfh = logging.FileHandler("./log/multikeys_server_user.log")
userfh.setLevel(logging.INFO)
userch = logging.StreamHandler()
userch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s--%(name)s--%(levelname)s - %(message)s")
userch.setFormatter(formatter)
userfh.setFormatter(formatter)
userlogger.addHandler(userch)
userlogger.addHandler(userfh)
# 系统运行logger配置
syslogger = logging.getLogger("MULTIKEYS_SERVER_SYSTEM")
syslogger.setLevel(logging.INFO)
sysfh = logging.FileHandler("./log/multikeys_server_system.log")
sysfh.setLevel(logging.INFO)
sysch = logging.StreamHandler()
sysch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s--%(name)s--%(levelname)s - %(message)s")
sysch.setFormatter(formatter)
sysfh.setFormatter(formatter)
syslogger.addHandler(sysch)
syslogger.addHandler(sysfh)

# 获取首页信息
def main(request):
    if request.method == 'GET':
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        # 获取设备数量
        sql = "SELECT count(*) FROM keys_set"
        cursor.execute(sql)
        num = cursor.fetchone()
        # 获取已配置列表
        sql = " SELECT inputID,inputName,ip,status FROM keys_set"
        cursor.execute(sql)
        array = cursor.fetchall()
        for i in array:
            i = list(i)
            status_dict[i[0]][1] = i[1]
        conn.close()
        return render(request, 'system/main.html', {'setnum': num[0], 'form': list(status_dict.values())})


# 获取已配置列表
def configed(request):
    if request.method == 'GET':
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = " SELECT inputName,ip,description,inputID FROM keys_set"
        cursor.execute(sql)
        form_configed = cursor.fetchall()
        conn.close()
        return render(request, 'system/configed.html', {'form': form_configed})


# 获取未配置列表
def free(request):
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    cursor = conn.cursor()
    if request.method == 'GET':
        sql = " SELECT dev_ID,description FROM input_select WHERE free = 1"
        cursor.execute(sql)
        form_free = cursor.fetchall()
        conn.close()
        return render(request, 'system/free.html', {'form': form_free})


# 获取当前配置信息
def config(request):
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    key_list = range(1, 13)
    key_name_list = []
    for index in range(1, 13):
        key_name_list.append("按键" + str(index))
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            info_dict = form.cleaned_data
            status = info_dict['status']
            cursor = conn.cursor()
            sql = " SELECT name,id FROM output_list "
            cursor.execute(sql)
            output_name = cursor.fetchall()
            sql = " SELECT name FROM template"
            cursor.execute(sql)
            form_template = cursor.fetchall()
            dict_keyname = {'1': info_dict['key1'], '2': info_dict['key2'], '3': info_dict['key3'], '4': info_dict['key4'],
                            '5': info_dict['key5'], '6': info_dict['key6'], '7': info_dict['key7'], '8': info_dict['key8'],
                            '9': info_dict['key9'], '10': info_dict['key10'], '11': info_dict['key11'], '12': info_dict['key12']}
            # 新建按键配置
            if status == 'new':
                data = json.dumps([' ', ' '])
                sql = "INSERT INTO keys_set (inputID, inputName, ip, description, keyName, status, " + \
                      "key1, key2, key3, key4, key5, key6, key7, key8, key9, key10, key11, key12," + \
                      "key1id, key2id, key3id, key4id, key5id, key6id, key7id, key8id, key9id, key10id, key11id, key12id) " + \
                      "values('" + info_dict['id'] + "','" + info_dict['name'] + "','" + info_dict['ip'] + "','" + info_dict['description'] + "','" + \
                      json.dumps(dict_keyname, ensure_ascii=False) + "','off'," + \
                      "'" + data + "','" + data + "','" + data + "','" + data + "','" + data + "','" + data + "','" + data + "','" + data + \
                      "','" + data + "','" + data + "','" + data + "','" + data + "','" + data + "','" + data + "','" + data + "','" + data + \
                      "','" + data + "','" + data + "','" + data + "','" + data + "','" + data + "','" + data + "','" + data + "','" + data + "')"
                try:
                    cursor.execute(sql)
                except Exception as e:
                    conn.close()
                    return render(request, 'system/config.html', {'name': info_dict['name'], 'id': info_dict['id'], 'form': form, 'status': 'new', 'alter': 'error'})
                else:
                    conn.commit()
                    sql = " UPDATE input_select SET free = 0 WHERE dev_ID = '"+info_dict['id']+"'"
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
                    status_dict[info_dict['id']] = [info_dict['id'], info_dict['name'], info_dict['ip'], 'off']
                    key_name_list = list(dict_keyname.values())
                    for index,keyname in enumerate(key_name_list):
                        if keyname == '':
                            key_name_list[index] = '按键' + str(index+1)
                    userlogger.info("创建按键配置： " + info_dict['name'])
                    return render(request, 'system/keyconfig.html', {'dict': info_dict, 'output_name': output_name, 'form_template': form_template,
                                                                     'key_list': key_list, 'key_name_list': key_name_list})
            # 编辑按键配置
            elif status == 'edit':
                sql = "UPDATE keys_set SET ip='"+info_dict['ip']+"',description='"+info_dict['description']+"',keyName='"+json.dumps(dict_keyname, ensure_ascii=False)+"' WHERE inputID='"+info_dict['id']+"'"
                try:
                    cursor.execute(sql)
                except Exception as e:
                    conn.close()
                    return render(request, 'system/config.html', {'name': info_dict['name'], 'id': info_dict['id'],
                                                                  'form': form, 'status': 'edit', 'alter': 'error'})
                else:
                    status_dict[info_dict['id']] = [info_dict['id'], info_dict['name'], info_dict['ip'], 'off']
                    conn.commit()
                    sql = "SELECT key1,key2,key3,key4,key5,key6,key7,key8,key9,key10,key11,key12,keyname FROM keys_set WHERE inputID='"+info_dict['id']+"'"
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
                    key_name_list = list(json.loads(val[12]).values())
                    conn.close()
                    userlogger.info("编辑按键配置： " + info_dict['name'])
                    return render(request, 'system/keyconfig.html',
                                  {'dict': info_dict, 'output_name': output_name, 'form_template': form_template,
                                   'key_list': key_list, 'key_name_list': key_name_list,
                                   'key1': key1, 'key2': key2, 'key3': key3, 'key4': key4, 'key5': key5, 'key6': key6,
                                   'key7': key7, 'key8': key8, 'key9': key9, 'key10': key10, 'key11': key11, 'key12': key12})
    else:
        form = ConfigForm()
        id = request.GET.get('id', default='10000000')
        name = request.GET.get('name', default='10000000')
        status = request.GET.get('status', default='10000000')
        # 新增设备配置
        if status == 'new':
            return render(request, 'system/config.html', {'name': name, 'id': id, 'form': form, 'status': 'new'})
        if status == 'edit':
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
            return render(request, 'system/config.html', {'name': val[1], 'id': val[0], 'form': form, 'dict': key_dict, 'status': 'edit'})


# 保存按键配置
def saveconf(request):
    if request.method == 'POST':
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        mes = request.POST['mes']
        key_set = json.loads(mes)
        status = request.POST['status']
        if status == 'new':
            userlogger.info("保存按键设置 ID： " + key_set['id'])
            sql = "UPDATE keys_set SET keyname='" + json.dumps(key_set['key_name'], ensure_ascii=False) + \
                  "',key1='"+ json.dumps(key_set['key1'], ensure_ascii=False) + "',key2='" + json.dumps(key_set['key2'], ensure_ascii=False) + \
                  "',key3='"+ json.dumps(key_set['key3'], ensure_ascii=False) + "',key4='"+ json.dumps(key_set['key4'], ensure_ascii=False) + \
                  "',key5='"+ json.dumps(key_set['key5'], ensure_ascii=False) + "',key6='"+ json.dumps(key_set['key6'], ensure_ascii=False) + \
                  "',key7='"+ json.dumps(key_set['key7'], ensure_ascii=False) + "',key8='"+ json.dumps(key_set['key8'], ensure_ascii=False) + \
                  "',key9='"+ json.dumps(key_set['key9'], ensure_ascii=False) + "',key10='"+ json.dumps(key_set['key10'], ensure_ascii=False) + \
                  "',key11='"+ json.dumps(key_set['key11'], ensure_ascii=False) + "',key12='"+ json.dumps(key_set['key12'], ensure_ascii=False) + \
                  "',key1id='"+json.dumps(key_set['key1_id']) + "',key2id='"+json.dumps(key_set['key2_id']) + \
                  "',key3id='"+json.dumps(key_set['key3_id']) + "',key4id='"+json.dumps(key_set['key4_id']) + \
                  "',key5id='"+json.dumps(key_set['key5_id']) + "',key6id='"+json.dumps(key_set['key6_id']) + \
                  "',key7id='"+json.dumps(key_set['key7_id']) + "',key8id='"+json.dumps(key_set['key8_id']) + \
                  "',key9id='"+json.dumps(key_set['key9_id']) + "',key10id='"+json.dumps(key_set['key10_id']) + \
                  "',key11id='"+json.dumps(key_set['key11_id']) + "',key12id='"+json.dumps(key_set['key12_id']) + \
                  "' WHERE inputID ='" + key_set['id'] + "'"
            cursor.execute(sql)
            conn.commit()
            # 获取终端IP
            sqlip ="SELECT ip FROM keys_set where inputID='"+key_set['id']+"'"
            cursor.execute(sqlip)
            ip = cursor.fetchone()
            conn.close()
            # 向终端发送按键设置
            data = {"method": "update", "data": {}}
            try:
                json_data = json.dumps(data)
                r = requests.post('http://'+ip[0]+':8888', data=json_data, timeout=http_timeout)
                syslogger.info("向终端发送按键设置 IP： " + ip[0])
            except Exception as e:
                syslogger.error("向终端发送按键配置异常 IP： " + ip[0])
                print(e)
            return JsonResponse({'code': 1, 'msg': 'success'})


# 删除配置
def conf_action(request):
    if request.method == 'GET':
        action = request.GET.get('action')
        id = request.GET.get('id')
        if action == 'delete':
            ip = request.GET.get('ip')
            conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
            cursor = conn.cursor()
            userlogger.info("删除按键配置： 输入ID：" + id)
            sql = "DELETE FROM keys_set WHERE inputID = '"+id+"';"
            cursor.execute(sql)
            conn.commit()
            sql = " UPDATE input_select SET free = 1 WHERE dev_ID = '"+id+"'"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            data = {"method": "update", "data": {}}
            try:
                json_data = json.dumps(data)
                r = requests.post('http://'+ip+':8888', data=json_data, timeout=http_timeout)
                syslogger.info("向终端发送按键配置删除信息： IP：" + ip)
            except Exception as e:
                print(e)
                syslogger.error("向终端发送按键配置异常： IP：" + ip)
            finally:
                del status_dict[str(id)]
                return HttpResponseRedirect("configed.html")


# 从模板加载配置
def loadtemp(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = " SELECT * FROM template WHERE name='"+name+"'"
        cursor.execute(sql)
        val = cursor.fetchone()
        key_name_list = list(json.loads(val[13]).values())
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
        userlogger.info("加载配置模板： " + name)
        return JsonResponse({'key_name_list': key_name_list, 'key1': key1, 'key2': key2, 'key3': key3, 'key4': key4, 'key5': key5, 'key6': key6,
                             'key7': key7, 'key8': key8, 'key9': key9, 'key10': key10, 'key11': key11, 'key12': key12})


# 获取模板列表
def template(request):
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    cursor = conn.cursor()
    if request.method == 'POST':
        pass
    else:
        sql = " SELECT * FROM template"
        cursor.execute(sql)
        form_template = cursor.fetchall()
        sql = " SELECT INPUTID,INPUTNAME,IP FROM KEYS_SET"
        cursor.execute(sql)
        input_list = cursor.fetchall()
    conn.close()
    return render(request, 'system/template.html', {'form': form_template, 'input_list': input_list})


# 新建模板
def new_temp(request):
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    cursor = conn.cursor()
    key_list = list(range(1, 13))
    key_name_list = []
    for index in range(1, 13):
        key_name_list.append("按键" + str(index))
    if request.method == 'GET':
        sql = " SELECT NAME,ID FROM output_list "
        cursor.execute(sql)
        output_name = cursor.fetchall()
        conn.close()
        return render(request, 'system/newtemp.html', {'output_name': output_name, 'key_list': key_list, 'key_name_list': key_name_list})


# 模板应用到输出
def deploy_temp(request):
    if request.method == 'POST':
        input_id = request.POST["inputId"]
        template_name = request.POST["templateName"]
        deploy_temp_action(input_id, template_name)
        # HTTP Response
        return JsonResponse({'code': 1, 'msg': 'success'})


def deploy_temp_action(input_id, template_name):
    # 根据模板名称获取按键配置
    key_set = {}
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    cursor = conn.cursor()
    sql = "SELECT * FROM key_set WHERE NAME = '" + template_name + "'"

    sql = "SELECT * FROM TEMPLATE WHERE NAME = '" + template_name + "'"
    cursor.execute(sql)
    conn.commit()
    temp = cursor.fetchall()[0]
    test = temp[13]
    key_set["key_name"] = temp[13]
    template = temp[1:13]
    for index, key in enumerate(template):
        keyid = str(index + 1)
        key_set["key" + keyid] = []
        key_set["key" + keyid + "_id"] = []
        name_list = []
        id_list = []
        key_config = key.replace('[', '').replace(']', '').replace(' ', '').replace('"', '').split(',')
        for index, output_name in enumerate(key_config):
            if output_name != '':
                sql = "SELECT ID FROM OUTPUT_LIST WHERE NAME = '" + output_name + "'"
                cursor.execute(sql)
                output_id = cursor.fetchall()[0][0]
                name_list.append(output_name)
                id_list.append(str(output_id))
            else:
                pass
        key_set["key" + keyid] = name_list
        key_set["key" + keyid + "_id"] = id_list
    # 更新按键设置存储
    sql = "UPDATE keys_set SET keyname='" + key_set['key_name'] + \
          "',key1='" + json.dumps(key_set['key1'], ensure_ascii=False) + "',key2='" + json.dumps(key_set['key2'],
                                                                                                 ensure_ascii=False) + \
          "',key3='" + json.dumps(key_set['key3'], ensure_ascii=False) + "',key4='" + json.dumps(key_set['key4'],
                                                                                                 ensure_ascii=False) + \
          "',key5='" + json.dumps(key_set['key5'], ensure_ascii=False) + "',key6='" + json.dumps(key_set['key6'],
                                                                                                 ensure_ascii=False) + \
          "',key7='" + json.dumps(key_set['key7'], ensure_ascii=False) + "',key8='" + json.dumps(key_set['key8'],
                                                                                                 ensure_ascii=False) + \
          "',key9='" + json.dumps(key_set['key9'], ensure_ascii=False) + "',key10='" + json.dumps(key_set['key10'],
                                                                                                  ensure_ascii=False) + \
          "',key11='" + json.dumps(key_set['key11'], ensure_ascii=False) + "',key12='" + json.dumps(key_set['key12'],
                                                                                                    ensure_ascii=False) + \
          "',key1id='" + json.dumps(key_set['key1_id']) + "',key2id='" + json.dumps(key_set['key2_id']) + \
          "',key3id='" + json.dumps(key_set['key3_id']) + "',key4id='" + json.dumps(key_set['key4_id']) + \
          "',key5id='" + json.dumps(key_set['key5_id']) + "',key6id='" + json.dumps(key_set['key6_id']) + \
          "',key7id='" + json.dumps(key_set['key7_id']) + "',key8id='" + json.dumps(key_set['key8_id']) + \
          "',key9id='" + json.dumps(key_set['key9_id']) + "',key10id='" + json.dumps(key_set['key10_id']) + \
          "',key11id='" + json.dumps(key_set['key11_id']) + "',key12id='" + json.dumps(
        key_set['key12_id']) + "' WHERE inputID ='" + input_id + "'"
    cursor.execute(sql)
    conn.commit()
    userlogger.info("将配置模板{}应用到输入{}".format(template_name, input_id))
    # 获取终端IP
    sqlip = "SELECT ip FROM keys_set where inputID='" + input_id + "'"
    cursor.execute(sqlip)
    ip = cursor.fetchone()
    conn.close()
    # 向终端发送按键设置
    data = {"method": "update", "data": {}}
    try:
        json_data = json.dumps(data)
        r = requests.post('http://' + ip[0] + ':8888', data=json_data, timeout=http_timeout)
        syslogger.info("向终端发送按键配置改变信息： IP：" + ip[0])
    except Exception as e:
        syslogger.error("向终端发送按键配置信息失败： IP：" + ip[0])
        print(e)


# 编辑模板
def temp_action(request):
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    cursor = conn.cursor()
    if request.method == 'GET':
        action = request.GET.get('action')
        name = request.GET.get('name')
        if action == 'delete':
            pass
        if action == 'edit':
            key_list = list(range(1, 13))
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
            key_name_list = list(json.loads(val[13]).values())
            sql = " SELECT NAME,ID FROM output_list "
            cursor.execute(sql)
            form = cursor.fetchall()
            conn.close()
            return render(request, 'system/edittemp.html', {'name': temp_name, 'key_list': key_list, 'key_name_list': key_name_list, 'output_name': form,
                                                            'key1': key1, 'key2': key2, 'key3': key3, 'key4': key4,
                                                            'key5': key5, 'key6': key6, 'key7': key7, 'key8': key8,
                                                            'key9': key9, 'key10': key10, 'key11': key11, 'key12': key12})


#删除模板
def delete_temp(request):
    if request.method == "POST" :
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'],
                                dsn=database['default']['DSN'])
        cursor = conn.cursor()
        temp_name = request.POST['name']
        # 判断该模板是否被任务使用
        sql = "SELECT * FROM task"
        cursor.execute(sql)
        task_list = cursor.fetchall()
        conn.commit()
        for task in task_list:
            task_name = task[0]
            task = json.loads(task[1]);
            for temp in task.values():
                if temp == temp_name:
                    conn.close()
                    return JsonResponse({'code': 2, 'msg': "该配置模板正在被任务模板 {} 使用".format(task_name)})
        # 删除模板
        sql = "DELETE FROM template WHERE name = '" + temp_name + "'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        userlogger.info("删除按键配置模板： " + temp_name)
        return JsonResponse({'code': 1, 'msg': 'success'})


# 保存模板
def save_temp(request):
    if request.method == 'POST':
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        mes = request.POST['mes']
        status = request.POST['status']
        tem_set = json.loads(mes)
        if status == 'new':
            sql = "INSERT INTO template (name,keyname,key1,key2,key3,key4,key5,key6,key7,key8,key9,key10,key11,key12) values('" +\
                  tem_set['name'] + "','" + json.dumps(tem_set['key_name'], ensure_ascii=False) + "','" +\
                  json.dumps(tem_set['key1'], ensure_ascii=False) + "','" + json.dumps(tem_set['key2'], ensure_ascii=False) + "','" +\
                  json.dumps(tem_set['key3'], ensure_ascii=False) + "','" + json.dumps(tem_set['key4'], ensure_ascii=False) + "','" +\
                  json.dumps(tem_set['key5'], ensure_ascii=False) + "','" + json.dumps(tem_set['key6'], ensure_ascii=False) + "','" +\
                  json.dumps(tem_set['key7'], ensure_ascii=False) + "','" + json.dumps(tem_set['key8'], ensure_ascii=False) + "','" +\
                  json.dumps(tem_set['key9'], ensure_ascii=False) + "','" + json.dumps(tem_set['key10'], ensure_ascii=False) + "','" +\
                  json.dumps(tem_set['key11'], ensure_ascii=False) + "','" + json.dumps(tem_set['key12'], ensure_ascii=False)+"')"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            userlogger.info("保存按键配置模板[新增]： " + tem_set['name'])
        elif status == 'edit':
            if tem_set['name'] == tem_set['old_name']:
                sql = "UPDATE template SET keyname='" + json.dumps(tem_set['key_name'], ensure_ascii=False) + "', key1='" + json.dumps(tem_set['key1'], ensure_ascii=False) + "',key2='"\
                  + json.dumps(tem_set['key2'], ensure_ascii=False) + "',key3='"+ json.dumps(tem_set['key3'], ensure_ascii=False)+"',key4='"\
                  + json.dumps(tem_set['key4'], ensure_ascii=False) +"',key5='"+ json.dumps(tem_set['key5'], ensure_ascii=False) +"',key6='"\
                  + json.dumps(tem_set['key6'], ensure_ascii=False) +"',key7='"+ json.dumps(tem_set['key7'], ensure_ascii=False) +"',key8='"\
                  + json.dumps(tem_set['key8'], ensure_ascii=False) +"',key9='"+ json.dumps(tem_set['key9'], ensure_ascii=False) +"',key10='"\
                  + json.dumps(tem_set['key10'], ensure_ascii=False) +"',key11='"+ json.dumps(tem_set['key11'], ensure_ascii=False) +"',key12='"\
                  + json.dumps(tem_set['key12'], ensure_ascii=False) +"' WHERE name='"+tem_set['name']+"'"
            else:
                sql = "UPDATE template SET keyname='" + json.dumps(tem_set['key_name'], ensure_ascii=False) + "', name='"+tem_set['name']+"',key1='" + json.dumps(tem_set['key1'], ensure_ascii=False) + "',key2='"\
                  + json.dumps(tem_set['key2'], ensure_ascii=False) + "',key3='"+ json.dumps(tem_set['key3'], ensure_ascii=False)+"',key4='"\
                  + json.dumps(tem_set['key4'], ensure_ascii=False) +"',key5='"+ json.dumps(tem_set['key5'], ensure_ascii=False) +"',key6='"\
                  + json.dumps(tem_set['key6'], ensure_ascii=False) +"',key7='"+ json.dumps(tem_set['key7'], ensure_ascii=False) +"',key8='"\
                  + json.dumps(tem_set['key8'], ensure_ascii=False) +"',key9='"+ json.dumps(tem_set['key9'], ensure_ascii=False) +"',key10='"\
                  + json.dumps(tem_set['key10'], ensure_ascii=False) +"',key11='"+ json.dumps(tem_set['key11'], ensure_ascii=False) +"',key12='"\
                  + json.dumps(tem_set['key12'], ensure_ascii=False) +"' WHERE name='"+tem_set['old_name']+"'"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            userlogger.info("保存按键配置模板[编辑]： " + tem_set['name'])
        return JsonResponse({'code': 1, 'msg': 'success'})


#根据名称获取配置模板信息
def get_temp_detail(request):
    if request.method == 'GET':
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        name = request.GET['name']
        sql = "SELECT * FROM template WHERE name='{}'".format(name)
        cursor.execute(sql)
        temp = cursor.fetchone()
        conn.close()
        return JsonResponse({'code': 1, 'msg': 'success', 'temp': temp})


#获取任务模板页面信息
def task(request):
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    cursor = conn.cursor()
    if request.method == 'GET':
        sql = " SELECT * FROM task"
        cursor.execute(sql)
        task_list = cursor.fetchall()
        sql = "SELECT * FROM keys_set"
        cursor.execute(sql)
        input_list = cursor.fetchall()
    conn.close()
    return render(request, 'system/task.html', {'form': task_list, 'input_list': input_list})


#新增/编辑任务模板
def task_edit(request):
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    cursor = conn.cursor()
    if request.method == 'GET':
        sql = "SELECT * FROM keys_set"
        cursor.execute(sql)
        input_list = cursor.fetchall()
        sql = "SELECT * FROM template"
        cursor.execute(sql)
        temp_list = cursor.fetchall()
        task = {}
        if request.GET['action'] == 'new':      #新建任务模板
            conn.close()
            return render(request, 'system/task_edit.html', {'task': task, 'input_list': input_list, 'temp_list': temp_list, 'action': "new"})
        elif request.GET['action'] == 'edit':    #编辑任务模板
            name = request.GET['name']
            sql = "SELECT * FROM task WHERE name = '" + name + "'"
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.close()
            task_name = result[0][0]
            task_info_dict = json.loads(result[0][1])
            task_info_dict = zip(task_info_dict.keys(), task_info_dict.values())
            task_info_list = []
            for item in task_info_dict:
                task_info_list.append(item)
            task = [task_name, task_info_list]
            return render(request, 'system/task_edit.html', {'task': task, 'input_list': input_list, 'temp_list': temp_list, 'action': "edit"})


#保存任务模板
def task_save(request):
    if request.method == 'POST':
        mes = request.POST['mes']
        status = request.POST['status']
        name = request.POST['name']
        task_set = json.loads(mes)
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        if status == 'new':
            sql = "SELECT * FROM task WHERE name = '" + name + "'"
            cursor.execute(sql)
            task = cursor.fetchall()
            if len(task) != 0:
                return JsonResponse({'code': 2, 'msg': '任务名称重复，请重新创建！'})
            sql = "INSERT INTO task (name,taskmap) values('" + name + "','" + json.dumps(task_set) + "')"
            cursor.execute(sql)
            conn.commit()
            userlogger.info("保存任务模板[新增]： " + name)
        elif status == 'edit':
            old_name = request.POST['old_name']
            sql = "UPDATE task SET name='{}',taskmap='{}' where name='{}'".format(name, json.dumps(task_set), old_name)
            cursor.execute(sql)
            conn.commit()
            userlogger.info("保存任务模板[编辑]： " + name)
        conn.close()
        return JsonResponse({'code': 1, 'msg': 'success'})


#删除任务模板
def task_delete(request):
    if request.method == 'POST':
        task = request.POST['name']
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = "DELETE FROM task WHERE name = '{}'".format(task)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        userlogger.info("删除任务模板： " + task)
        return JsonResponse({'code': 1, 'msg': 'success'})


#应用任务模板
def task_deploy(request):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        userlogger.info("应用任务模板： " + task_name)
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = "SELECT * FROM task WHERE name = '{}'".format(task_name)
        cursor.execute(sql)
        task_info = cursor.fetchone()
        conn.commit()
        task_info = json.loads(task_info[1])
        for id, temp in task_info.items():
            if temp != '':
                deploy_temp_action(id, temp)
        conn.close()
        return JsonResponse({'code': 1, 'msg': 'success'})


def getinfo(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
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
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
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
            sql = "UPDATE usradmin SET username='{}',passwd='{}' where id={}".format(name,newpwd,muser[0])
            cursor.execute(sql)
            conn.commit()
            userlogger.info("更新用户账号信息")
            return HttpResponseRedirect('/')
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
        syslogger.info("多按键设备请求配置信息： IP：" + data_ip)
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
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
        syslogger.info("多按键设备请求设备检查： IP：" + ip)
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
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
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
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
                status_val = status_dict[str(id)]
                status_val[3] = 'on'
                status_dict[str(id)] = status_val
            elif method == 'client disconnect':
                status_val = status_dict[str(id)]
                status_val[3] = 'off'
                status_dict[str(id)] = status_val
            else:
                return JsonResponse({'code': 1, 'msg': 'error'})
    return JsonResponse({'code': 1, 'msg': 'success'})


# 获取所有多key终端状态
def get_status(request):
    val = list(status_dict.values())
    return JsonResponse({'statusform': val})


# 获取转发状态
def tcpstatus(request):
    if request.method == "POST":
        pass
    else:
        try:
            data = {"method": "keeplive", "data": "ping"}
            json_data = json.dumps(data)
            val = []
            r = requests.post("http://0.0.0.0:8080", data=json_data, timeout=http_timeout)
            if r.status_code == 200:
                val.append('on')
                return JsonResponse({"tcpstatus": val})
            else:
                val.append('off')
                return JsonResponse({"tcpstatus": val})
        except Exception as e:
            val.append('off')
            return JsonResponse({"tcpstatus": val})


# 获取管理平台连接状态
def server_status(request):
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    cursor = conn.cursor()
    data_json = {}
    if request.method == 'POST':
        mes = json.loads(request.POST['MultiK'])
        data = mes['data']
        method = mes['method']
        ip = data['ip']
        if method == 'server connect':
            sql = "Delete from web_status where id = 1"
            cursor.execute(sql)
            sql = "INSERT INTO web_status(ip,id,status) values ('{}',{},'{}')".format(ip, 1,'on')
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return JsonResponse({'code': 1, 'msg': 'success'})
        if method =="server disconnect":
            sql = "UPDATE web_status SET status='off' WHERE id=1"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return JsonResponse({'code': 1, 'msg': 'success'})
        else:
            return JsonResponse({'code': 1, 'msg': 'error'})
    else:
        sql = "SELECT ip,status FROM web_status WHERE id=1"
        cursor.execute(sql)
        array = cursor.fetchall()
        for i in array:
            i = list(i)
            data_json[i[0]] = i
        return JsonResponse({"tcpstatus": list(data_json.values())})


# 获取CPU内存使用率
def getServerUsage(request):
    server_info = {}
    cpu_percent = psutil.cpu_percent(interval=1)
    server_info["cpu_usage"] = "%i%%" % cpu_percent
    virtual_memory = psutil.virtual_memory()
    used_memory = virtual_memory.used / 1024 / 1024 / 1024
    free_memory = virtual_memory.free / 1024 / 1024 / 1024
    server_info["mem_usage"] = "%0.2fG/%0.2fG" % (used_memory, used_memory + free_memory)
    return JsonResponse({'serverInfo': server_info, 'msg': 'success'})


# 更新、获取管理平台配置
def save_ip(request):
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    cursor = conn.cursor()
    if request.method == 'POST':
        ip = request.POST.get("ip")
        port = request.POST.get("description")
        sql = "Delete from web_status where id = 1"
        cursor.execute(sql)
        sql = "INSERT INTO web_status(id,ip,port) values ({}, '{}', {})".format(1, ip, port)
        cursor.execute(sql)
        conn.commit()
        userlogger.info("更新可视化管理平台配置信息")
        dir = os.getcwd()
        file_path = dir + '/conf/configip.ini'
        with open(file=file_path, mode="w", encoding="utf-8") as f:
            f.write(f'[serverinfo]\nip = {ip}\nport = {port}')
        data = {"method": "update server configure", "data": {"ip": ip, "port": port}}
        json_data = json.dumps(data)
        try:
            r = requests.post("http://0.0.0.0:8080", data=json_data, timeout=http_timeout)
        except Exception as e:
            userlogger.error("更新可视化管理平台配置信息失败")
            print(e)
        finally:
            conn.close()
            return HttpResponseRedirect('/system/createip.html')
    else:
        form = IpForm()
        json_dict = {}
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = "SELECT ip,status FROM web_status"
        cursor.execute(sql)
        array = cursor.fetchall()
        conn.close()
        for i in array:
            i = list(i)
            json_dict[i[0]] = i
        return render(request, 'system/createip.html', {'form': form, 'tcpstatus': list(json_dict.values()), 'status': 0})


# 获取输入设备
def devices(request):
    if request.method == "POST":
        pass
    else:
        json_data = []
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = " SELECT inputID,inputName,description,ip FROM keys_set"
        cursor.execute(sql)
        array = cursor.fetchall()
        for i in array:
            json_data.append({
                "id": str(i[0]),
                "name": i[1],
                "description": i[2],
                "ip": i[3],
                "status": status_dict[str(i[0])][3]+'line'
            })
        return JsonResponse({"data":json_data})


# 报告ip冲突
def ip_conflict(request):
    if request.method == "POST":
        mes = json.loads(request.POST['MultiK'])
        data = mes['data']
        ip = data['ip']
        syslogger.info("发现多按键设备IP冲突： {}".format(ip))
        msgQueue.put("发现多按键设备IP冲突（{}）".format(ip))
        return JsonResponse({'code': 1, 'msg': 'success'})


# 消费消息队列
def consume_msg(request):
    if request.method == "POST":
        msg = ''
        if not msgQueue.empty():
            msg = msgQueue.get()
        return JsonResponse({'code': 1, 'msg': msg})


# 更新输入输出通道名称
'''
-------------------------------------------------------------------------
request：[URL:http://localhost:8000/system/updateChannel Method：POST, Content-Type：application/json]
{
    "data": [
        {"old_name": "测试输入1", "new_name": "新输入1", "type": "input"},
        {"old_name": "测试输出1", "new_name": "新输出1", "type": "output"}
    ]
}
-------------------------------------------------------------------------
response:
{
    "code": 200,
    "msg": "更新成功"
}

{
    "code": 500,
    "msg": "更新失败"
}
-------------------------------------------------------------------------
'''
def update_channel(request):
    try:
        if request.method == "POST":
            # data1 = json.loads(request.POST['MultiK'])
            data = json.loads(bytes.decode(request.body, encoding='utf-8'))["data"]
            # data = data1['data']
            for item in data:
                if item["type"] == "INPUT":
                    update_input(item)
                elif item["type"] == "OUTPUT":
                    update_output(item)
                else:
                    syslogger.error("未知通道类型")
                    return JsonResponse({'code': 501, 'msg': "更新失败"})
            syslogger.info("接收到输入输出设备名称变更请求")
            msgQueue.put("输入输出设备名称已更新！")
            return JsonResponse({'code': 200, 'msg': "更新成功"})
    except Exception as e:
        syslogger.error("更新输入输出名称失败")
        print(e)
        return JsonResponse({'code': 500, 'msg': "更新失败"})


def update_input(info):
    syslogger.info("更新输入通道名称： ID"+str(info['id']) + info['old_name'] + "->" + info['new_name'])
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    cursor = conn.cursor()
    try:
        sql = " UPDATE input_select SET description = '" + info['new_name'] + "' WHERE dev_id = '" + str(info['id']) + "'"
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    try:
        sql = " UPDATE keys_set SET inputname = '" + info['new_name'] + "' WHERE id = '" + str(info['id']) + "'"
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()


def update_output(info):
    syslogger.info("更新输出通道名称：ID " +str(info['id']) + info['old_name'] + "->" + info['new_name'])
    conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
    cursor = conn.cursor()
    # 更新output_list
    try:
        sql = " UPDATE output_list SET name = '" + info['new_name'] + "' WHERE id = '" + str(info['id']) + "' "
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    # 更新keys_set
    try:
        sql = " SELECT * FROM keys_set "
        cursor.execute(sql)
        configes = cursor.fetchall()
        for conf in configes:   #遍历每一条config
            conf = list(conf)[6:18]
            update_info = handle_key_config(conf, info)
            if len(update_info) > 0:
                sql_1 = 'UPDATE keys_set SET ';sql_2 = '';sql_3 = ''
                for key,val in update_info.items():
                    sql_2 += 'ID =' + "'" + val["id"] + "' "
                    sql_3 += 'KEY' + str(key) + '=' + "'" + val["new_name"] + "' "
                sql = sql_1 + sql_3 + 'WHERE ' + sql_2
                cursor.execute(sql)
                conn.commit()
    except Exception as e:
        print(e)
    # 更新template
    try:
        sql = " SELECT * FROM template "
        cursor.execute(sql)
        templates = cursor.fetchall()
        for template in templates:   #遍历每一条template
            template = list(template)[1:13]
            update_info = handle_key_config(template, info)
            if len(update_info) > 0:
                sql_1 = 'UPDATE template SET '
                sql_2 = ''
                sql_3 = ''
                for key,val in update_info.items():
                    sql_2 += 'KEY' + str(key) + '=' + "'" + val["old"] + "' "
                    sql_3 += 'KEY' + str(key) + '=' + "'" + val["new"] + "' "
                sql = sql_1 + sql_3 + 'WHERE ' + sql_2
                cursor.execute(sql)
                conn.commit()
    except Exception as e:
        print(e)
    conn.close()


'''
处理key配置的字符串替换
输入:key配置list
输出:整理后的需要更改的key配置字典
    { 1: {'old': '["测试输出1","测试输入12","测试输入123"]', 'new': '["新输出1","测试输入12","测试输入123"]'}}
'''
def handle_key_config(conf, info):
    update_info = {}
    for index, old_key in enumerate(conf):  # 遍历每个KEY配置
        new_key = old_key.replace('"' + info["old_name"] + '"', '"' + info["new_name"] + '"')
        if old_key != new_key:
            update_info[index + 1] = {"old": old_key, "new": new_key}
    return update_info


# 查看用户操作日志
def log_user(request):
    if request.method == 'GET':
        return render(request, 'system/log_user.html', {})


#查看系统运行日志
def log_system(request):
    if request.method == 'GET':
        return render(request, 'system/log_system.html', {})


# 根据类型获取操作日志
def get_log_info(request):
    if request.method == 'GET':
        log = []
        type = request.GET["type"]
        str = request.GET["str"]
        try:
            if type == "user":
                path = "./log/multikeys_server_user.log"
            elif type == "system":
                path = "./log/multikeys_server_system.log"
            else:
                return JsonResponse({'code': 200, 'log': log})
            with open(path, 'r') as f:
                content = f.readlines()
                content.reverse()
                content = content[0:500]  # 默认前端最多显示500条
                for line in content:
                    if str != '' and not line.__contains__(str):
                        continue
                    else:
                        if line.__contains__("--INFO"):
                            line = '<div class="panel panel-info" style="border-width:medium;">' + line + '</div>'
                        elif line.__contains__("--WARRING"):
                            line = '<div class="panel panel-warring" style="border-width:medium;">' + line + '</div>'
                        elif line.__contains__("--ERROR"):
                            line = '<div class="panel panel-danger" style="border-width:medium;">' + line + '</div>'
                        log.append(line)
        except Exception as e:
            log = []
        return JsonResponse({'code': 200, 'log': log})


# 下载用户操作日志文件
def user_log_download(request):
    try:
        syslogger.info("下载用户操作日志")
        response = FileResponse(open('./log/multikeys_server_user.log', 'rb'))
        response['content-type'] = "application/octet-stream"
        response['content-Disposition'] = "attachment; filename= server_user.log"
        return response
    except Exception:
        syslogger.error("下载用户操作日志失败")

# 下载系统运行日志文件
def sys_log_download(request):
    try:
        syslogger.info("下载系统运行日志")
        response = FileResponse(open('./log/multikeys_server_system.log', 'rb'))
        response['content-type'] = "application/octet-stream"
        response['content-Disposition'] = "attachment; filename= server_system.log"
        return response
    except Exception:
        syslogger.error("下载系统运行日志失败")

