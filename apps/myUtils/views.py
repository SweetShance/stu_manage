from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core import serializers
import numpy as np
from stu_table.utils import ExcelOperate
from stu_table.models import Coolege, Stu_class, Stu_base_message, Transition
from user.models import Monitor, Teacher
from .utils import aboout_sno_message, new_conn_mysql, search_fields_list



class Error(View):
    def get(self, request):
        context = {}
        from_url = request.GET.get('from_url')
        if from_url:
            context['from_url'] = from_url
        else:
            context['from_url'] = '/'

        return render(request, template_name="html/error_no_premission.html", context=context)


class Delete_data(View):
    def post(self, request):
        conn = new_conn_mysql()
        cur = conn.cursor()
        try:
            data_list = eval(request.POST.get('data'))
            for i in data_list:
                cur.execute("delete from stu_table_stu_base_message where sno='%s'"%i)
        except TypeError:
            cur.execute("delete from stu_table_stu_base_message where sno='%s'"%request.POST.get('data'))
        except NameError:
            cur.execute("delete from stu_table_stu_base_message where sno='%s'"%request.POST.get('data'))

        conn.commit()
        cur.close()
        conn.close()
        return JsonResponse({"status": 'yes', 'count': len(data_list)})

class Alert_stu_data(View):
    def get(self, request):
        sno = request.GET.get('sno')
        zh_fields_list, data_tuple = aboout_sno_message(sno)
        field_data = zip(zh_fields_list, data_tuple)
        # 所在学院的所有班级
        index = zh_fields_list.index("学院")
        class_index = zh_fields_list.index("班级")
        this_coolege = Coolege.objects.filter(coolege_name=data_tuple[index])[0]
        if str(request.user.user_role) == "班长":
            cooleges = Coolege.objects.filter(pk = Monitor.objects.get(username=request.user).class_name.coolege_name_id)
            class_names = Stu_class.objects.filter(class_name = Monitor.objects.get(username=request.user).class_name)
        elif str(request.user.user_role) == "老师":
            cooleges = Coolege.objects.filter(pk = Teacher.objects.get(username=request.user).class_name.coolege_name_id)
            class_names = this_coolege.class_name.all()
        else:
            cooleges = Coolege.objects.all()
            class_names = this_coolege.class_name.all()
        this_class = Stu_class.objects.filter(class_name=data_tuple[class_index])[0]
        context = {
            "field_datas": field_data,
            "class_names": class_names,
            "this_class": this_class,
            "this_coolege": this_coolege,
            "cooleges": cooleges
        }
        return render(request, template_name="stu_table/alter_form.html", context=context)

    def post(self, request):
        
        data = {}
        values = []
        print(request.POST)
        if not request.POST:
            data['status'] = '失败'
        else:
            for k,value in request.POST.items():
                if k == "学院":
                    continue
                else:
                    values.append(value)
            # 插入到数据库
            fields_list, cur, conn = search_fields_list()
            #查询原来的
            cur.execute('select * from stu_table_stu_base_message where sno=%s'%values[0])
            arr2 = []
            for i in cur.fetchall()[0]:
                arr2.append(str(i))
            # 找出两个列表不相等的
            arr1 = np.array(values)
            arr2 = np.array(arr2)
            index = np.arange(0, len(values))
            not_eq_index = index[arr1 != arr2]
            fields_index = fields_list.index('coolege_name')
            fields_list.pop(fields_index)
            fields_list[fields_list.index('class_name')] = 'stu_class_id'
            print(fields_list)
            print(values)
            print(not_eq_index)
            # 字符串拼接
            str_sentence = ""
            if not_eq_index is not None:
                for i in not_eq_index:
                    if i != not_eq_index[-1]:
                        str_sentence += fields_list[i]  + "=" + '"'+ values[i] + '"' + ","
                    else:
                        str_sentence += fields_list[i] + "=" + '"'+ values[i]+ '"'
                # 跟新数据
                # print(str_sentence)
                cur.execute("update stu_table_stu_base_message set %s where sno='%s'"%(str_sentence, values[0]))
                conn.commit()
                cur.close()
                conn.close()
                data['status'] = '成功'
            else:
                data['status'] = '数据没有改动'
            
        
        return JsonResponse(data)


class GetClass(View):
    def post(self, request):
        pk = request.POST.get('pk')
        if request.user.user_role.role_name == "班长":
            class_objs = Stu_class.objects.filter(class_name = Monitor.objects.get(username=request.user).class_name)
            data = serializers.serialize("json", class_objs)
        else:
            if pk:
                class_objs = Coolege.objects.get(pk=pk).class_name.all()
                data = serializers.serialize("json", class_objs)
            else:
                data = ""
        return JsonResponse(data, safe=False)

class GetColleges(View):
    def get(self, request):
        objs = Coolege.objects.all()
        # 将其序列化
        data = serializers.serialize("json", objs)
        print(data)
        return JsonResponse(data, safe=False)

class AddStu(View):
    def post(self, request):
        data = {}
        sno = request.POST.get('学号')
        sname = request.POST.get("姓名")
        sex = request.POST.get("性别")
        if sno:
            if not Stu_base_message.objects.filter(sno=sno):
                if sname:
                    # 添加数据
                    if sex:
                        values = []
                        for k,v in request.POST.items():
                            if k != "学院":
                                if v == "":
                                    values.append('null')
                                else:
                                    try:
                                        values.append(int(v))
                                    except ValueError:
                                        values.append(v)
                            
                        values = str(values).replace('[','').replace(']','').replace("\'n", 'n').replace("l\'",'l')
                        
                        conn = new_conn_mysql()
                        cur = conn.cursor()
                        sentence = "insert into stu_table_stu_base_message() values(%s)"%values
                        print(sentence)
                        cur.execute(sentence)
                        conn.commit()
                        cur.close()
                        conn.close()
                        data['status'] = 'success'
                    else:
                        data['status'] = "sex"
                else:
                    data['status'] = "sname"
            else: 
                data['status'] = "该学生已存在"
        else:
            data['status'] = "sno"
        return JsonResponse(data)

class AddField(View):
    def post(self, request):
        field = request.POST.get('text')
        this_type = request.POST.get('type') 
        data = {}
        # ex = ExcelOperate()
        if field is not None:
            #查询当前字段自否已经在转换列表中了
            transObj = Transition.objects.filter(zh_name=field)
            if transObj:
                print(transObj)
                # 判断当前字段是否已经存在已有字段中了
                # 链接数据库
                conn = new_conn_mysql()
                cur = conn.cursor()
                cur.execute("select column_name from information_schema.columns where table_name='stu_table_stu_base_message' and table_schema='manage'")
                already_fields = cur.fetchall()
                if (transObj.first().eng_name,) in already_fields:
                    data['status'] = '字段或类似字段已存在'
                    cur.close()
                    conn.close()
                else:
                    ex = ExcelOperate()
                    ex.create_field(transObj.first().eng_name, this_type)
            else:
                ex = ExcelOperate()
                # 翻译
                eng_name = ex.transition(field)
                ex.insert_transform_table(eng_name, field)
                ex.create_field(eng_name, this_type)
                data['static'] = '成功'
            
        #
        return JsonResponse(data)

    def get(self, request):
        return HttpResponse('ye')


class Search(View):
    def post(self, request):
        print(request.POST)
        return JsonResponse({'a':'A'})