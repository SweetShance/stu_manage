from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
import xlrd
from user.models import Monitor, Profile, Teacher
from .models import File, mymodel_delete
from .utils import ExcelOperate, search_fields_list, search_zh_fields_list, paginator_utils


# Create your views here.
class Merge(View):
    def get(self, request):
        return render(request, template_name="html/upload.html", context={})

    def post(self, request):
        data = {'static': 'error'}
        try:
            file_name = request.FILES['file']
            file_path = File.objects.create(files=file_name)
            # 将数据插入到数据库表中
            ex = ExcelOperate()
            ex.file_name = "/home/shance/project/intelligent_form/intelligent_form"+file_path.files.url
            ex.mian()
            instance = file_path
            sender = File
            mymodel_delete(sender,instance)
            if ex.error:
                data['static'] = ex.error
                data['data_list'] = ex.query_list 
                data['query_data'] = ex.query_data
                data['title'] = ex.zh_name
            else: 
                data['static'] = 'success'
            
            # print(data['data_list'])
        except  BaseException:
            pass
        
        return JsonResponse(data)

# 异常信息显示
class Anomaly(View):
    def post(self, request):
        # print(request.POST)
        # print(request.POST.get('data_list'))
        context = {}
        context['data_list'] = eval(request.POST.get('data_list'))
        context['static'] = request.POST.get('static')
        context['eng_list'] = eval(request.POST.get('eng_list'))
        context['title'] = eval(request.POST.get('title'))
        # print(type(eval(request.POST.get('data_list'))))
        # print(request.POST.get('static'))
        # 异常信息展示页面
        return render(request, template_name='stu_table/anomaly.html', context=context)
    
    def get(self, request):
        # 异常信息展示页面
        return render(request, template_name='stu_table/anomaly.html', context={})

# 补录数据
class Replenish(View):
    def post(self, request):
        data = {'status': 'error'}
        data_list = eval(request.POST.get('data'))
        query_list = eval(request.POST.get('eng_list'))
        try:
            ex = ExcelOperate()
            ex.eng_name = eval(query_list)[0]
            
            ex.data_type = eval(query_list)[1]
            for i in data_list:
                ex.row_data = eval(i)
                ex.binding_name_data()
                ex.update_data(1)
            data['status'] = 'success'
            data['count'] = len(data_list)
        except BaseException:
            pass
        
        return JsonResponse(data)
    
    def get(self, request):
        print(request.GET)
        return HttpResponse("yes")

# 信息编辑
class Message_edit(View):
    def get(self, request):
        data_tuple = ""
        fields_list, cur = search_fields_list()
        field_list_str = str(fields_list).replace('[', "").replace("]", "").replace("'","")
        # 如果身份是 管理员
        if str(request.user.user_role) == '管理员':
            search_sentence = "select %s from stu_table_stu_base_message A inner join stu_table_stu_class B on A.stu_class_id = B.id inner join stu_table_coolege C on B.coolege_name_id = C.id"%(field_list_str)
            cur.execute(search_sentence)
            data_tuple = cur.fetchall()
        # 如果身份是辅导员
        if str(request.user.user_role) == '老师':
            objs = Teacher.objects.filter(username=request.user)
            if objs:
                obj = obj[0]
                search_sentence = "select %s from stu_table_stu_base_message A inner join stu_table_stu_class B on A.stu_class_id = B.id inner join stu_table_coolege C on B.coolege_name_id = C.id where C.id = %s"%(field_list_str, obj.class_name_id)
                cur.execute(search_sentence)
                data_tuple = cur.fetchall()
        # 如果身份是班长
        if str(request.user.user_role) == '班长':
            # 获取班长班级 id
            objs = Monitor.objects.filter(username=request.user)
            if objs:
                obj = objs[0]
                # class_name_id = obj.class_name_id
                # 获取字段
                
                # 三表联合查询
                search_sentence = "select %s from stu_table_stu_base_message A inner join stu_table_stu_class B on A.stu_class_id = B.id inner join stu_table_coolege C on B.coolege_name_id = C.id where B.id = %s" %(field_list_str, obj.class_name_id);
                cur.execute(search_sentence)
                data_tuple = cur.fetchall()
                # 获取学生信息表的字段名:
                # cur.excute("select column_name from information_schema.columns where table_name='stu_table_stu_base_message' and table_schema='manage'")
                # search_fields_list()
        count = len(data_tuple)
        field_names = search_zh_fields_list(fields_list)
        page = request.GET.get('page')
        data_tuple = paginator_utils(data_tuple, page)
        context = {
            'field_names': field_names,
            'data_tuples': data_tuple,
            'count': count,
        }

        return render(request, template_name="html/stu-message-list.html", context=context)

    def post(self, request):
        pass