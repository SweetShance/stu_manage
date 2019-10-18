from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout
from django.views.generic import View
from django.db.models import Max
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from myUtils.utils import session_add_permission
from user.models import Permission,User_role, Profile
from stu_table.utils import paginator_utils
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


class LogOut(View):
    def get(self, request):
        if request.user:
            logout(request)
            return redirect('login')

class Register(View):
    def post(self, request):
        data = {}
        # 注册用户
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        name = request.POST.get('name')
        role = User_role.objects.get(role_name="学生")
        user = Profile.objects.filter(username=username)
        if user:
            data['status'] = "用户名已存在"
        else:
            user = Profile.objects.filter(email = email)
            if user:
                data['status'] = '该邮箱已被注册'
            else:   
                user = Profile.objects.create(username=username,password=password, email=email, name=name, user_role=role)
                login(request, user)
                data['status'] = '注册成功'
                data['username'] = username
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

# 角色管理 start
class RoleManagement(View):
    def get(self, request):
        role_name = request.GET.get('pk')
        if not role_name:
            # 获取素权限列表
            role_objs = User_role.objects.all()
            # 分页
            count = role_objs.count()
            #分页
            
        else:
            role_objs = User_role.objects.filter(role_name__contains=role_name )
            if role_objs:
                count = role_objs.count()
            else:
                count = 0
        page = request.GET.get('page')
        role_data = paginator_utils(role_objs, page, 15)
        context = {
            'count': count,
            'role_data':role_data,

        }

        return render(request, template_name="html/admin-role.html", context=context)

class RoleDelete(View):
    def post(self, request):
        pk = request.POST.get('pk')
        data = request.POST.get('values')
        dic = {}
        if data:
            dic['count'] = len(eval(data))
            for pk in eval(data):
                obj = get_object_or_404(User_role, pk=pk)
                obj.delete()
            dic['status'] = 'success'
        else:
            obj = get_object_or_404(User_role, pk=pk)
            obj.delete()
            dic['status'] = 'success'
        return JsonResponse(dic)

class RoleAdd(View):
    def get(self, request):
        permissions = Permission.objects.all()
        context = {
            'permissions': permissions,
        }
        return render(request, template_name="html/role-add.html", context=context)

    def post(self, request):
        role_name = request.POST.get('role_name')
        pk_list = request.POST.get('value')
        desc = request.POST.get('desc')
        # 得到最大的身份码
        max_role_code = User_role.objects.all().aggregate(Max('role_code'))['role_code__max']
        new_role = User_role.objects.create(role_code=max_role_code+1 ,role_name=role_name, role_description=desc)
        for pk in eval(pk_list):
            obj = get_object_or_404(Permission, pk=pk)
            new_role.permission.add(obj)
        # 创建
        return redirect('roleadd')

class RoleEdit(View):
    def get(self, request):
        pk = request.GET.get('pk')
        obj = get_object_or_404(User_role, pk=pk)
        permissions = Permission.objects.all()
        obj_permissions = obj.permission.all()
        
        context = {
            'obj': obj,
            'permissions': permissions,
            'obj_permissions': obj_permissions,
        }
        return render(request, template_name = 'html/role_edit.html', context=context)
        
    def post(self, request):
        pk = request.POST.get('pk')
        role_name = request.POST.get('role_name')
        permission_pk_list = request.POST.get('value')
        desc = request.POST.get('desc')
        # 获取对象
        obj = get_object_or_404(User_role, pk=pk)
        obj.role_name = role_name
        
        for i in eval(permission_pk_list):
            print(i)
            per_obj = get_object_or_404(Permission, pk=i)
            obj.permission.add(per_obj)
        obj.role_description = desc
        obj.save()

        return JsonResponse({'status': 'success'})


# 角色管理 end



class Permiclassify(View):
    def get(self, request):
        return render(request, template_name="html/admin-cate.html", context={})

class PermiManagement(View):
    def get(self, request):
        permission_list =  Permission.objects.all()
        count = permission_list.count()
        #分页
        page = request.GET.get('page')
        permission_data = paginator_utils(permission_list, page, 15)
        context = {
            "permission_list":permission_data,
            "count": count,
        }
        return render(request, template_name="html/admin-rule.html", context=context)
    

class PermissionAdd(View):
    def post(self, request):
        # 数据保存
        rule_name = request.POST.get('rule_name')
        rule_url = request.POST.get('rule_url')
        desc = request.POST.get('desc')
        Permission.objects.create(permission_name=rule_name, url=rule_url, permission_description=desc)
        return redirect('permiManagement')
    
class PermissionDelete(View):
    def post(self, request):
        pk = request.POST.get('pk')
        data = request.POST.get('values')
        # # print(request.POST)
        # # 删除多个
        dic = {}
        if data:
            dic['count'] = len(eval(data))
            for v in eval(data):
                print(v)
                obj = get_object_or_404(Permission, pk=v)
                obj.delete()
            dic['status'] = 'success'

        else:
            obj = get_object_or_404(Permission, pk=pk)
            obj.delete()
            dic['status'] = 'success'
        # print('yes')
        return JsonResponse(dic)
    
    def get(self, request):
        # print(request.POST)
        return HttpResponse('yes')
    

class PermissionEdit(View):
    def get(self, request):
        pk = request.GET.get('pk')
        obj = get_object_or_404(Permission, pk=pk)
        context = {
            'obj': obj
        }
        return render(request, template_name = 'permission_edit.html', context=context)
    
    def post(self, request):
        pk = request.POST.get('pk')
        rule_name = request.POST.get('rule_name')
        rule_url = request.POST.get('rule_url')
        desc = request.POST.get('desc')
        # 获取对象
        obj = get_object_or_404(Permission, pk=pk)
        obj.permission_name = rule_name
        obj.url = rule_url
        obj.permission_description = desc
        obj.save()
        return JsonResponse({'status': 'success'})


