from django.db import models

class Notification(models.Model):
    tile = models.CharField(verbose_name="标题", max_length=100)
    content = models.TextField(verbose_name="内容", max_length=500)
    about_file = models.FileField(verbose_name="相关文件", blank=True, null=True)
    update_time = models.DateField(verbose_name="发布时间", auto_now_add=True)
    is_active = models.BooleanField(verbose_name="是否展示", default=False)

    def __str__(self):
        return "%s"%self.tile

    class Meta:
        verbose_name_plural = "通知"