from django.contrib import admin
from .models import Stu_base_message, Stu_class, Coolege, Transition

# Register your models here.

@admin.register(Stu_base_message)
class Stu_base_messageAdmin(admin.ModelAdmin):
    list_display = ['sno', 'sname', 'sex', 'stu_class']


@admin.register(Stu_class)
class Stu_class_Admin(admin.ModelAdmin):
    list_display = ["id", "class_name", "coolege_name", 'add_time']


@admin.register(Coolege)
class Coolege_Admin(admin.ModelAdmin):
    list_display = ['id', 'coolege_name', 'add_time']

@admin.register(Transition)
class TransitionAdmin(admin.ModelAdmin):
    list_display = ['zh_name', 'eng_name']

