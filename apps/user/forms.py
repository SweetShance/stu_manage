from django import forms
import re

class PersonalDetailsForm(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={'class': 'layui-input', 'readonly':True,}))
    name = forms.CharField(label="姓名", widget=forms.TextInput(attrs={'class': 'layui-input',"lay-verify":"required", 'placeholder':'输入姓名', 'required':True}))
    phone = forms.CharField(label="手机号", widget=forms.TextInput(attrs={'class': 'layui-input', 'placeholder':'输入手机号'}))
    email = forms.EmailField(label="邮箱", widget=forms.EmailInput(attrs={'class': 'layui-input','placeholder':'输入邮箱'}))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) == 11:
            phone = re.search('1[0-9]{10}$', phone)
            if phone:
                return phone
        raise forms.ValidationError('请填写正确的手机号')