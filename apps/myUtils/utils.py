from user.models import Profile
from stu_table.utils import new_conn_mysql, search_fields_list, search_zh_fields_list
# Create your views here.
def session_add_permission(request, username):
    # 获取当前对象对应的身份
    permissions = Profile.objects.get(username=username).user_role.permission.all()
    permission_list = []
    for permission in permissions:
        permission_list.append(permission.url)
    # print(, "&&&&&&&&&&&")
    # print(type(list(permission_list)))
    request.session['permission_list'] = {}
    for permission in permission_list:
        request.session['permission_list'][permission] = permission 
    request.session.set_expiry(0)

def aboout_sno_message(sno):
    # 链接数据库
    fields_list, cur, conn = search_fields_list()
    field_list_str = str(fields_list).replace('[', "").replace("]", "").replace("'","")
    zh_fields_list = search_zh_fields_list(fields_list)
    # 返回 字段名和游标
    # 三表联合查询数据
    # search_sentence = "select %s from stu_table_stu_base_message A inner join stu_table_stu_class B on A.stu_class_id = B.id inner join stu_table_coolege C on B.coolege_name_id = C.id where A.sno=%s" %(field_list_str, sno);
    search_sentence = "select %s from stu_table_stu_base_message A left join stu_table_stu_class B on A.stu_class_id = B.id left join stu_table_coolege C on B.coolege_name_id = C.id where A.sno=%s" %(field_list_str, sno);
    cur.execute(search_sentence)
    this_data = cur.fetchall()
    if this_data:
        data_tuple = this_data[0]
    else:
        data_tuple = ()
    cur.close()
    conn.close()
    return zh_fields_list, data_tuple