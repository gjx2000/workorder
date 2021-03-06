# Generated by Django 2.0.4 on 2019-08-27 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0003_auto_20190825_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlowConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='工单名称')),
                ('callback', models.CharField(max_length=64, verbose_name='回调地址')),
                ('customfield', models.TextField(verbose_name='自定义字段')),
                ('description', models.TextField(verbose_name='描述')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name_plural': '工单模板',
            },
        ),
    ]
