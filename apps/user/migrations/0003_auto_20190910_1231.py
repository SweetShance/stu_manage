# Generated by Django 2.2 on 2019-09-10 12:31

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stu_table', '0001_initial'),
        ('user', '0002_auto_20190910_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='刘勇', max_length=20, verbose_name='姓名'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user_role',
            name='role_description',
            field=models.TextField(blank=True, max_length=200, verbose_name='角色描述'),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('coolege_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stu_table.Coolege')),
            ],
            options={
                'verbose_name_plural': '教师',
            },
            bases=('user.profile',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stu_table.Stu_class')),
            ],
            options={
                'verbose_name_plural': '班长',
            },
            bases=('user.profile',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]