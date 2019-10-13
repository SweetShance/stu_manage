from django.db import models
from django.contrib.auth.models import AbstractUser
from stu_table.models import Stu_class, Coolege
# Create your models here.

# 用户表
class Profile(AbstractUser):
    name = models.CharField(verbose_name="姓名", max_length=20)
    phone = models.CharField(verbose_name="电话", max_length=11)
    user_role = models.ForeignKey('User_role', verbose_name='身份', \
        on_delete=models.DO_NOTHING, null=True, blank=True, related_name="username")
    class Meta:
        verbose_name_plural = '管理员'
    
# 班长用户表
class Monitor(Profile):
    class_name = models.ForeignKey(Stu_class, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "班长"

    def __str__(self):
        return "%s"%self.name


class Teacher(Profile):
    coolege_name = models.ForeignKey(Coolege, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "教师"
    
    def __str__(self):
        return "%s"%self.name
    



#  角色表
class User_role(models.Model):
    role_code = models.IntegerField(verbose_name="用户码", help_text="用于表示用户权限, 1 代表管理员,2 代表辅导员, 3代表班长", )
    role_name = models.CharField(verbose_name="角色名称", max_length=20)
    permission = models.ManyToManyField(to='Permission', verbose_name="权限")
    role_description = models.TextField(verbose_name="角色描述", max_length=200, blank=True)
    create_time = models.DateField(verbose_name='创建时间', auto_now=True)
    class Meta:
        verbose_name_plural = "角色信息"

    def __str__(self):
        return "%s" %self.role_name


# 权限表
class Permission(models.Model):
    permission_name = models.CharField(verbose_name="权限名称",max_length=50)
    url = models.CharField(verbose_name="权限路由", max_length=100)
    permission_description = models.TextField(verbose_name="权限描述", max_length=200, null=True, blank=True)
    class Meta:
        verbose_name_plural = "权限信息"
    
    def __str__(self):
        return "%s"%self.permission_name





# 


