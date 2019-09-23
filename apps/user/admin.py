from django.contrib import admin
from .models import Profile, Permission, User_role, Monitor, Teacher

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username','name', 'email', 'phone', 'user_role', 'date_joined', 'last_login']
    readonly_fields = ('password',)
    fieldsets = (
        ('修改用户', {
            'fields': ('username', 'password')
        }),
        ('基本信息', {
            'classes': ('collapse', 'wide', 'extrapretty'),  # 'collapse','wide', 'extrapretty'
            'fields': ('name','user_role', 'email','phone', 'date_joined', 'last_login', 'is_active'),
        }),
    )

# @admin.register(Permission)
# class PermissionAdmin(admin.ModelAdmin):
#     list_display = ['permission_name', ]
    # fields = ('username', 'password', 'user_role', 'email','phone', 'date_joined', 'last_login', 'is_active')

@admin.register(User_role)
class User_roleAdmin(admin.ModelAdmin):
    list_display = ['role_name', 'role_description', 'create_time']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['permission_name', 'permission_description']


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ['username','name', 'email', 'phone', 'user_role','class_name', 'date_joined', 'last_login']
    readonly_fields = ('password',)
    fieldsets = (
        ('修改用户', {
            'fields': ('username', 'password')
        }),
        ('基本信息', {
            'classes': ('collapse', 'wide', 'extrapretty'),  # 'collapse','wide', 'extrapretty'
            'fields': ('name', 'user_role', 'email','phone','class_name', 'date_joined', 'last_login', 'is_active'),
        }),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['username','name', 'email', 'phone', 'user_role','coolege_name', 'date_joined', 'last_login']
    readonly_fields = ('password',)
    fieldsets = (
        ('修改用户', {
            'fields': ('username', 'password')
        }),
        ('基本信息', {
            'classes': ('collapse', 'wide', 'extrapretty'),  # 'collapse','wide', 'extrapretty'
            'fields': ('name','user_role', 'email','phone','coolege_name', 'date_joined', 'last_login', 'is_active'),
        }),
    )

