import hashlib, random
import urllib
import httplib2
import xlrd
import MySQLdb
from django.core.paginator import Paginator
from .models import Transition, Stu_base_message, Stu_class


class ExcelOperate():
    def __init__(self):
        self.sheet = ""
        self.zh_name = []
        self.eng_name = []
        self.row_data = []
        self.name_data = {}
        self.data_type = []
        self.query_list = []
        self.query_data = []
        self.file_name = ""
        
        self.error = ""
        
    
    # 汉语转英文
    def transition(self, your_words):
        appid = '20190817000327288' #你的appid
        secretKey = 'QwHBwxGEZc2rsgYDZ3T0' #你的密钥
        httpClient = None
        myurl = '/api/trans/vip/translate'
        q = your_words
        fromLang = 'zh'
        toLang = 'en'
        salt = random.randint(32768, 65536)
        sign = appid+q+str(salt)+secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode('utf8'))
        sign = m1.hexdigest()
        myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
        try:
            httpClient = httplib2.HTTPConnectionWithTimeout('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            b = response.read().decode('utf-8')
            return(eval(b)['trans_result'][0]['dst'])
            # print(eval(b)['trans_result'][0]['dst'])
        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()
    
    # 打开文件/ 默认读表格里的第一个表 sheet1
    def open_file(self, file_name):
        rexcel = xlrd.open_workbook(filename=file_name)
        # 读取表格内的表
        self.sheet = rexcel.sheet_by_index(0)

    # 读取excel文件
    def read_excel_row(self, row):
        try:
            self.row_data = self.sheet.row_values(row)
            return self.row_data
        except IndexError:
            return False
    
    #  如到对照表中
    def insert_transform_table(self, eng_name, zh_name):
        Transition.objects.create(zh_name=zh_name, eng_name=eng_name)
    
    # 链接数据库
    def conn_mysql(self):
        conn = MySQLdb.Connect(
                    host='127.0.0.1',
                    port=3306,
                    user='root',
                    passwd='root',
                    db='manage',
                    charset="utf8"
                )
        return conn

    # 创建字段
    def create_field(self, field, filedType):
        conn = self.conn_mysql()
        cur = conn.cursor()
        if filedType == 1:
            cur.execute("alter table stu_table_stu_base_message add %s varchar(100) " %field)
        elif filedType == 2:
            cur.execute("alter table stu_table_stu_base_message add %s int " %field)
        elif filedType == 3:
            cur.execute("alter table stu_table_stu_base_message add %s DATA " %field)
        elif filedType == 4:
            cur.execute("alter table stu_table_stu_base_message add %s tinyint " %field)
        else:
            cur.execute("alter table stu_table_stu_base_message add %s varchar(100) " %field)
        conn.commit()
        cur.close()
        conn.close()
    
    # 更新数据
    def update_data(self, default=None):
        # 根据学号筛选
        
        # 获取该模型的所有字段名
        # fields_data = obj._meta.fields
        # # 将数据转换为字典
        # data_dict = obj.__dict__
        conn = self.conn_mysql()
            # 更新数据
        cur = conn.cursor()
        # 信息异常修改处理
        objects= Stu_base_message.objects.filter(sno=self.name_data['sno'])
        if not default and  objects:
            obj =  objects.first()
            if obj.sname != None and obj.sname !=self.name_data['sname']:
                self.query_list.append(self.row_data)
                self.query_data.append(self.eng_name)
                self.query_data.append(self.data_type)
                self.error = "姓名"
                return '姓名'
            if obj.sex != None and obj.sex != self.name_data['sex']:
                self.query_list.append(self.row_data)
                self.query_data.append(self.eng_name)
                self.query_data.append(self.data_type)
                self.error = "性别"
                # print(self.row_data)
                return '性别'

            if str(obj.stu_class) != self.name_data['stu_class'] and obj.stu_class != None:
                self.query_list.append(self.row_data)
                self.query_data.append(self.eng_name)
                self.query_data.append(self.data_type)
                self.error = "班级"
                return '班级'
        # obj = Stu_base_message.objects.filter(sno=self.name_data['sno']).first()
        if not  objects:
            # 如果没有就创建
            obj = Stu_base_message.objects.create(sno=self.name_data['sno'])
        else:
            obj =  objects.first()
        for field in self.name_data:
             # 判断 字段的位置
            index = self.eng_name.index(field)
            
            if field == "stu_class":
                stu_id = Stu_class.objects.get(class_name__contains=self.name_data[field]).id
                cur.execute("update stu_table_stu_base_message set stu_class_id = %s where sno=%s"%(stu_id, self.name_data['sno']))
            
            
            # print("update stu_table_stu_base_message set %s = '%s' where sno=%s"%(field, self.name_data[field], self.name_data['sno']))
           
            # 更新数据
            elif self.data_type[index] == 2 or self.data_type[index] == 3:
                cur.execute("update stu_table_stu_base_message set %s = %s where sno=%s"%(field, self.name_data[field], self.name_data['sno']))
                
            else:
                cur.execute("update stu_table_stu_base_message set %s = '%s' where sno=%s"%(field, self.name_data[field], self.name_data['sno']))
                
                # cur.execute("update stu_table_stu_base_message set %s = '%s' where sno=%s"%(field, self.name_data[field], self.name_data['sno']))
            conn.commit()
        cur.close()
        conn.close()
        # 保存导数据库
        # obj.save()

    # 生成字典
    def binding_name_data(self):
        for key, value in zip(self.eng_name, self.row_data):
            self.name_data[key] = value


    def mian(self):
        self.open_file(self.file_name)
        self.zh_name = self.read_excel_row(0)
        # 读取excel数据类型
        
        # 读取类型
        for num, i in enumerate(self.row_data):
            excel_type=self.sheet.cell(1, num).ctype
            self.data_type.append(excel_type)
        #  获取英文名字列表, 是根据excel表格数据的顺序来的
        for number, title in enumerate(self.row_data):
            obj= Transition.objects.filter(zh_name=title).first()
            if obj:
                self.eng_name.append(obj.eng_name)
            else:
                eng_name = self.transition(title).strip().replace(" ", "_")
                # 创建字段
                # conn = self.conn_mysql()
                self.create_field(eng_name, self.data_type[number])
                # 插入到对照表数据
                Transition.objects.create(zh_name=title, eng_name=eng_name)
                self.eng_name.append(eng_name)
        # 循环读取表格数据
        a = 1
        Tag = True
        while Tag:
            Tag = self.read_excel_row(a)
            if Tag == False:
                break
            # 实现字典
            self.binding_name_data()
            self.update_data()
            a += 1
            


def new_conn_mysql():
    conn = MySQLdb.Connect(
                    host='127.0.0.1',
                    port=3306,
                    user='root',
                    passwd='root',
                    db='manage',
                    charset="utf8"
                )
    return conn

def search_fields_list():
    conn = new_conn_mysql()
    cur = conn.cursor()
    # 查询 学生表 所有字段
    cur.execute("select column_name from information_schema.columns where table_name='stu_table_stu_base_message' and table_schema='manage'")
    fields = cur.fetchall()
    fields_list = []
    for i in fields:
        fields_list.append(i[0])
    # 加入班级
    index = fields_list.index('stu_class_id')
    fields_list[index] = "class_name"
    # 加入学院
    fields_list.insert(index, "coolege_name")
    return fields_list, cur


def search_zh_fields_list(fields_list):
    zh_list = []
    for field in fields_list:
        zh_name = Transition.objects.get(eng_name=field).zh_name
        zh_list.append(zh_name)
    
    return zh_list


def paginator_utils(data_list, page):
    # 设置一页内容显示多少, 一页显示50条数据
    paginator = Paginator(data_list, 5)
    # 获取页码
    page_of_data = paginator.get_page(page)

    return page_of_data