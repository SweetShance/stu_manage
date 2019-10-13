from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
import re
from stu_table.utils import paginator_utils
from stu_table.models import Coolege, Stu_class
from .models import Monitor, Teacher, Profile
from .models import User_role, Profile
from .forms import PersonalDetailsForm


# Create your views here.
class UserList(View):
    def get(self, request):
        user_code = request.user.user_role.role_code
        user_list = []
        if user_code == 1:
            user_list = Profile.objects.all()
        else:
            role_list =  User_role.objects.filter(role_code__gt=user_code)
            
            # 获取角色对应的用户
            for role_obj in role_list:
                objs = role_obj.username.all()
                for user_obj in objs:
                    user_list.append(user_obj)
        page = request.GET.get('page')
        page_user_list  =  paginator_utils(user_list, page, 15)

        context = {
           'user_list': page_user_list,
           "count": len(user_list) 
        }
        return render(request, template_name="html/user-list.html", context=context)

    def post(self, request):
        username = request.POST.get('username')
        user_objs = Profile.objects.filter(username__contains=username)
        user_list = []
        for user_obj in user_objs:
            if user_obj.user_role.role_code > request.user.user_role.role_code:
                user_list.append(user_obj)
        context = {
            'user_list': user_list,
            "count": len(user_list) 
        }
        return render(request, template_name="html/user-list.html", context=context)


class ChangePassword(View):
    def get(self, request):
        pk = request.GET.get('pk')
        obj = get_object_or_404(Profile,pk=pk)
        return render(request, template_name="html/member-password.html", context={'obj':obj})

    def post(self, request):
        data = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        passwordAgain = request.POST.get('passwordAgain')
        if password == passwordAgain:
            obj = get_object_or_404(Profile, username=username)
            print(obj)
            obj.set_password(password)
            obj.save()
            data['status'] = '成功'
        else:
            data['status'] = '两次密码不一致'
        
        return JsonResponse(data)


class AddUser(View):
    def get(self, request):
        user_code = request.user.user_role.role_code
        if user_code == 1:
            user_roles = User_role.objects.all().order_by('-pk')
            # 所有学院
            colleges = Coolege.objects.all()
        else:
            user_roles = User_role.objects.filter(role_code__gt=user_code).order_by('-pk')
            colleges = Coolege.objects.filter(pk=Teacher.objects.get(username=request.user).coolege_name_id)
        context = {
           "user_roles": user_roles,
           'colleges': colleges,
        }
        return render(request, template_name="html/adduser.html", context=context)

    def post(self, request):
        data = {'status': "error"}
        user_role = request.POST.get('user_role')
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        college = request.POST.get('college')
        class_id = request.POST.get('class')
        user_obj = Profile.objects.filter(username=username)
        if user_obj:
                data['status'] = "用户已存在"
        else:
            if user_role == "班长":
                class_name_obj = get_object_or_404(Stu_class, pk=class_id)
                user_role_obj = get_object_or_404(User_role, role_name=user_role)
                Monitor.objects.create(username=username,name=name ,password=password, user_role=user_role_obj, class_name=class_name_obj)
                data['status'] = "success"
            elif user_role=="老师":
                college_obj = get_object_or_404(Coolege, pk=college)
                user_role_obj = get_object_or_404(User_role, role_name=user_role)
                Teacher.objects.create(username=username, name=name,password=password, user_role=user_role_obj,coolege_name=college_obj)
                data['status'] = "success"
            else:
                user_role_obj = get_object_or_404(User_role, role_name=user_role)
                Profile.objects.create(username=username, name=name,password=password, user_role=user_role_obj)
                data['status'] = "success"
        return JsonResponse(data)

class DeleteUser(View):
    def get(self, request):
        return HttpResponse('yes')

    def post(self, request):
        data = {}
        values = request.POST.get('values')
        value = request.POST.get('value')
        if values:
            for i in eval(values):
                print(i)
                user_obj = get_object_or_404(Profile, pk=i)
                print(user_obj)
                user_obj.delete()
                count = len(eval(values))
                data['status'] = 'success'
                data['count'] = count
        elif value:
            user_obj = get_object_or_404(Profile, pk=value)
            user_obj.delete()
            data['status'] = 'success'

        return JsonResponse(data)


class PersonalDetails(View):
    def get(self, request):
        personalForm = Profile.objects.filter(username=request.user)
        context = {
            "personalForm":personalForm
        }
        return render(request, template_name="personaldetails.html", context=context)

    def post(self, request):
        data = {}
        print(request.POST)
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        try:
            print(username)
            obj = get_object_or_404(Profile, username=username)
            obj.name = name
            obj.email = email
            obj.phone = phone
            obj.save()

        except expression as identifier:
            pass
        
        return JsonResponse({'status':'yes'})
        


        
        