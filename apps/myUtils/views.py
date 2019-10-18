from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.generic import View
from django.core import serializers
import numpy as np
import xlwt
from io import BytesIO
from stu_table.utils import ExcelOperate
from stu_table.models import Coolege, Stu_class, Stu_base_message, Transition, File
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
        this_coolege = Coolege.objects.filter(coolege_name=data_tuple[index])
        if this_coolege:
            this_coolege = this_coolege[0]
        if str(request.user.user_role) == "班长":
            cooleges = Coolege.objects.filter(pk = Monitor.objects.get(username=request.user).class_name.coolege_name_id)
            if this_coolege:
                class_names = Stu_class.objects.filter(class_name = Monitor.objects.get(username=request.user).class_name)
            else:
                class_names = ""
        elif str(request.user.user_role) == "老师":
            cooleges = Coolege.objects.filter(pk = Teacher.objects.get(username=request.user).coolege_name_id)
            if this_coolege:
                class_names = this_coolege.class_name.all()
            else:
                class_names = ""
        else:
            cooleges = Coolege.objects.all()
            if this_coolege:
                class_names = this_coolege.class_name.all()
            else:
                class_names = ""
        this_class = Stu_class.objects.filter(class_name=data_tuple[class_index])
        if this_class:
            this_class = this_class[0]
        else:
            this_class = ""
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
            cur.execute('select * from stu_table_stu_base_message where sno="%s"'%values[0])
            result = cur.fetchall()
            if not result:
                cur.execute('insert into stu_table_stu_base_message(sno, sname, sex) values("%s","%s","%s")'%(values[0], values[1], values[2]))
                conn.commit()
                cur.execute('select * from stu_table_stu_base_message where sno=%s'%values[0])
                result = cur.fetchall()

        
            arr2 = []
            for i in result[0]:
                arr2.append(str(i))
            # 找出两个列表不相等的
            arr1 = np.array(values)
            arr2 = np.array(arr2)
            index = np.arange(0, len(values))
            not_eq_index = index[arr1 != arr2]
            fields_index = fields_list.index('coolege_name')
            fields_list.pop(fields_index)
            fields_list[fields_list.index('class_name')] = 'stu_class_id'
            # 字符串拼接
            str_sentence = ""
            if len(not_eq_index) > 0:
                for i in not_eq_index:
                    if i != not_eq_index[-1]:
                        str_sentence += fields_list[i]  + "=" + '"'+ values[i] + '"' + ","
                    else:
                        str_sentence += fields_list[i] + "=" + '"'+ values[i]+ '"'
                # 跟新数据
                # print(str_sentence)

                cur.execute("update stu_table_stu_base_message set %s where sno='%s'"%(str_sentence, values[0]))
                conn.commit()
                data['status'] = '成功'
            else:
                data['status'] = '数据没有改动'
            cur.close()
            conn.close()
            
        
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

class ShareGetClass(View):
    def post(self, request):
        pk = request.POST.get('pk')
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


class ImportDataToexcel(View):
    def post(self, request):
        field_str_list= request.POST.get('field')
        role = request.user.user_role.role_name
         # 读取对应的英文
        zh_field_list = eval(field_str_list)

        eng_field_list = []
        for field in zh_field_list:
            eng_field = Transition.objects.get(zh_name=field).eng_name
            eng_field_list.append(eng_field)
        conn = new_conn_mysql()
        cur = conn.cursor()
        field_list_str = str(eng_field_list).replace('[', "").replace("]", "").replace("'","")
        if role == "管理员":
            search_sentence = "select %s from stu_table_stu_base_message A left join stu_table_stu_class B on A.stu_class_id = B.id left join stu_table_coolege C on B.coolege_name_id = C.id" %(field_list_str)
        elif role == "老师":
            cooleges = Coolege.objects.filter(pk = Teacher.objects.get(username=request.user).coolege_name_id)
            search_sentence = "select %s from stu_table_stu_base_message A left join stu_table_stu_class B on A.stu_class_id = B.id left join stu_table_coolege C on B.coolege_name_id = C.id where C.coolege_name='%s'" %(field_list_str, cooleges[0] )
        elif role == "班长":
            class_names = Stu_class.objects.filter(class_name = Monitor.objects.get(username=request.user).class_name)
            search_sentence = "select %s from stu_table_stu_base_message A left join stu_table_stu_class B on A.stu_class_id = B.id left join stu_table_coolege C on B.coolege_name_id = C.id where B.class_name='%s'" %(field_list_str, class_names[0])
        # 读出数据
        cur.execute(search_sentence)
        data = cur.fetchall()
        # 制定excel文件
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename='+"city"+'.xls'
        wb = xlwt.Workbook(encoding = 'utf-8')
        worksheet = wb.add_sheet('sheet1')
        # 写表头
        for num, title in enumerate(zh_field_list):
            print(num, title)
            worksheet.write(0, num, title)
        for row, row_data in enumerate(data):
            for col, col_data in enumerate(row_data):
                worksheet.write(row+1, col, col_data)
        # 设置HTTPResponse的类型
        """导出excel表"""
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response


class CombinedExcel(View):
    def get(self, request):
        return render(request, template_name="html/manyExcel.html", context={})
    
    def post(self, request):
        return JsonResponse({'status': 'yes'})