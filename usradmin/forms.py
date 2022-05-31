from django import forms
import hashlib
import sqlite3
import STPython

class NameForm(forms.Form):
    usrname = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='密码', max_length=100)



    def clean(self):
        username=self.cleaned_data['usrname']
        password=self.cleaned_data['password']
        m = password + "{{sdtzzq}}"
        pw = hashlib.md5(m.encode())


        # conn = sqlite3.connect('db.sqlite3')
        conn = STPython.connect('SYSDBA','szoscar55')
        cursor = conn.cursor()
        sql = " SELECT username,passwd FROM usradmin"
        cursor.execute(sql)
        val = cursor.fetchall()
        muser = val[0]
        mpw = val[0]

        if (muser[0] == username)&(mpw[1] == pw.hexdigest()):
            pass
        else:
             raise forms.ValidationError(u"用户名或密码错误，请重新输入")

        conn.close()

        return self