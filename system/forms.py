import hashlib
import sqlite3
from multikeys import settings
from django import forms
import STPython

database = settings.DATABASES

class ConfigForm(forms.Form):
    id = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'true'}), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'true'}), required=False)
    ip = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '必填项', 'class': 'single_line'}), required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key3 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key4 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key5 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key6 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key7 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key8 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key9 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key10 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key11 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    key12 = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)
    status = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), required=False)


class UsrForm(forms.Form):
    usrname = forms.CharField(label='用户名', max_length=100)
    old_password = forms.CharField(widget=forms.PasswordInput, label='原密码', max_length=100)
    new_password = forms.CharField(widget=forms.PasswordInput, label='新密码', max_length=100)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput, label='新密码', max_length=100)
    def clean(self):
        old_password = self.cleaned_data['old_password']
        new_password = self.cleaned_data['new_password']
        new_password_confirm = self.cleaned_data['new_password_confirm']
        if(new_password == old_password):
            raise forms.ValidationError(u"新密码与原密码相同，请重新输入")
        elif(new_password != new_password_confirm):
            raise forms.ValidationError(u"两次输入的新密码不一致，请重新输入")
        m = old_password + "{{sdtzzq}}"
        pw = hashlib.md5(m.encode())
        conn = STPython.connect(user=database['default']['NAME'], password=database['default']['PASSWD'], dsn=database['default']['DSN'])
        cursor = conn.cursor()
        sql = " SELECT * FROM usradmin "
        cursor.execute(sql)
        val = cursor.fetchall()
        mpw = val[0][2]
        if (mpw == pw.hexdigest()):
            pass
        else:
             raise forms.ValidationError(u"原密码错误，请重新输入")
        conn.close()
        return self.cleaned_data


class IpForm(forms.Form):
    """
    这里是闫翔宇做的deMO，
    实现的功能是配置ip 端口号的功能
    """
    ip = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'single_line'}), label='ip', required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), label='端口', required=True)
    user = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), label='USER', required=True)
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'single_line'}), label='PASSWORD', required=True)
    dns = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '000.000.000.000:00000/XXXXXX', 'class': 'single_line'}), label='DSN', required=True)
