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

