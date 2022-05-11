import hashlib
import sqlite3
from django import forms

class ConfigForm(forms.Form):
    ip = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'必填项','class':'single_line'}), required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key1 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key2 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key3 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key4 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key5 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key6 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key7 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key8 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key9 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key10 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key11 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    key12 = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)
    id = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'true'}),required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'true'}),required=False)
    status = forms.CharField(widget=forms.TextInput(attrs={'class':'single_line'}), required=False)


class UsrForm(forms.Form):
    usrname = forms.CharField(label='用户名', max_length=100)
    old_password = forms.CharField(widget=forms.PasswordInput, label='原密码', max_length=100)
    new_password = forms.CharField(widget=forms.PasswordInput, label='新密码', max_length=100)



    def clean(self):

        password=self.cleaned_data['old_password']
        m = password + "{{sdtzzq}}"
        pw = hashlib.md5(m.encode())


        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        sql = " SELECT str FROM usradmin "
        cursor.execute(sql)
        val = cursor.fetchall()
        mpw = val[1]

        if (mpw[0] == pw.hexdigest()):
            pass
        else:
             raise forms.ValidationError(u"原密码错误，请重新输入")

        conn.close()

        return self.cleaned_data


"""
这里是闫翔宇做的deMO，
实现的功能是配置ip 端口号的功能
"""

class IpForm(forms.Form):
    ip = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '必填项', 'class': 'single_line'}),label='ip',  required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), label='端口', required=False)

