# Generated by Django 2.1.1 on 2020-06-18 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0023_auto_20200618_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='open_time',
            field=models.DateTimeField(verbose_name='제안서 오픈 시간'),
        ),
    ]
