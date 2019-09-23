from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from myUtils.utils import session_add_permission
from .forms import LoginForm

class Login(View):
    def get(self, request):
        loginForm = LoginForm()
        context = {
            'loginForm': loginForm,
        }
        return render(request, template_name="login.html", context=context)
    
    def post(self, request):
        data = {'status': ''}
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            error = loginForm.cleaned_data.get('error')
            # 提交成功
            data['status'] = "提交成功"
            if error:
                data['errormessage'] = error
                return JsonResponse(data)
            else:
                user = loginForm.cleaned_data.get('user')
                login(request, user)
                request.session['user'] = user.username
                request.session.set_expiry(0)
                data["status"] = "登录成功"
                # 将权限列表加入服务器
                session_add_permission(request, user.username)
                return JsonResponse(data)
        else:
            data['status'] = "提交失败"
            return JsonResponse(data)

class Register(View):
    def post(self, request):
        data = {}
        return JsonResponse(data)


class Index(View):
    def get(self, request):
        # if request.user.is_authenticated:
        #     print('yes')
        return render(request, template_name="index.html", context={})
        # else:
        #     return redirect('/')

    def post(self, request):
        return render(request, template_name="index.html", context={})

    

class Welcome(View):
    def get(self, request):
        return render(request, template_name="html/welcome.html", context={})
    


    
class AdminManagement(View):
    def get(self, request):
        return render(request, template_name="html/admin-list.html", context={})


class RoleManagement(View):
    def get(self, request):
        return render(request, template_name="html/admin-role.html", context={})
    
class Permiclassify(View):
    def get(self, request):
        return render(request, template_name="html/admin-cate.html", context={})

class PermiManagement(View):
    def get(self, request):
        return render(request, template_name="html/admin-rule.html", context={})

    


