from django.urls import path
from .views import UserList, ChangePassword, AddUser, DeleteUser, PersonalDetails

app_name = 'user'
urlpatterns = [
    path('userlist', UserList.as_view(), name='userlist'),
    path('changepassword', ChangePassword.as_view(), name='changepassword'),
    path('adduser', AddUser.as_view(), name="adduser"),
    path('deleteuser', DeleteUser.as_view(), name='deleteuser'),
    path('personaldetails', PersonalDetails.as_view(), name="personaldetails")
]