from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.

class Stu_base_message(models.Model):
    sno = models.CharField(verbose_name="学号", max_length=50, primary_key=True)
    sname = models.CharField(verbose_name="姓名", max_length=20)
    choice_list = [('男', '男'),
                   ('女', '女')]
    sex = models.CharField(verbose_name="性别", choices=choice_list, max_length=1)

    stu_class = models.ForeignKey('Stu_class', verbose_name="班级", on_delete=models.SET_NULL, null=True, blank=True )

    class Meta:
        verbose_name_plural = "学生信息"
        ordering = ['sno']
    
    def __str__(self):
        return "%s" %self.sno


class Stu_class(models.Model):
    class_name = models.CharField(verbose_name="班级", max_length=50)
    # 学院
    coolege_name = models.ForeignKey('Coolege', verbose_name="学院", on_delete=models.CASCADE, related_name="class_name")
    add_time = models.DateField(verbose_name="添加时间", auto_now_add=True)
    class Meta:
        verbose_name_plural = "班级"
    
    def __str__(self):
        return "%s"%self.class_name


class Coolege(models.Model):    
    coolege_name = models.CharField(verbose_name="学院", max_length=50)
    add_time = models.DateField(verbose_name="添加时间", auto_now_add=True, )
    class Meta:
        verbose_name_plural = "学院"
    
    def __str__(self):
        return "%s"%self.coolege_name

class Transition(models.Model):
    zh_name = models.CharField(verbose_name="中文名", max_length=100, primary_key=True)
    eng_name = models.CharField(verbose_name="英文名", max_length=100)

    class Meta:
        verbose_name_plural = "对照表"



class File(models.Model):
    files = models.FileField(upload_to="file_list")

# 用来删除上传的文件
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=File)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.files.delete(False)

