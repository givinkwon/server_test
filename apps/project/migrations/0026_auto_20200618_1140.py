# Generated by Django 2.1.1 on 2020-06-18 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0025_auto_20200618_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='open_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='제안서 오픈 시간'),
        ),
    ]