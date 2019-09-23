from user.models import Profile
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