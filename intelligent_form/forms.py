from django import forms
from django.contrib import auth

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(attrs={'id': 'user_name', 'placeholder': '用户名', }))
    password = forms.CharField(label="密码", max_length=20, widget=forms.PasswordInput(attrs={'id': 'password', 'placeholder': '密码'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # 用户认证
        user = auth.authenticate(username=username, password=password)

        if user is None:
            self.cleaned_data['error'] = '用户名或密码不正确'
            return self.cleaned_data
        else:
            self.cleaned_data['user'] = user
            # self.cleaned_data['error'] = ''
            return self.cleaned_data
