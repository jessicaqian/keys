from django.shortcuts import render
import sqlite3

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

    return render(request, 'system/free.html',{'form':form_free})