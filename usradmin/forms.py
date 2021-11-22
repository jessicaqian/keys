from django import forms
import hashlib
import configparser



class NameForm(forms.Form):
    usrname = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='密码', max_length=100)

    def clean(self):
        username=self.cleaned_data['usrname']
        password=self.cleaned_data['password']
        m = password + "{{sdtzzq}}"
        pw = hashlib.md5(m.encode())
        user = hashlib.md5(username.encode())
        cfg1 = "web.ini"
        conf = configparser.ConfigParser()
        conf.read(cfg1)
        muser = conf.get("importantinfo","important1")
        mpw = conf.get("importantinfo", "important2")
        if (muser == user.hexdigest())&(mpw == pw.hexdigest()):
            pass
        else:
             raise forms.ValidationError(u"用户名或密码错误，请重新输入")

        return self