# Generated by Django 2.1.1 on 2020-05-11 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20200507_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='add_meeting',
            field=models.BooleanField(default=False, null=True, verbose_name='추가로 미팅하기 여부'),
        ),
    ]
