# Generated by Django 2.2 on 2019-09-12 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stu_table', '0004_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stu_base_message',
            name='stu_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stu_table.Stu_class', verbose_name='班级'),
        ),
    ]