# Generated by Django 2.1.1 on 2020-05-25 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_auto_20200522_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content_bad',
            field=models.TextField(blank=True, null=True, verbose_name='계약 후기'),
        ),
        migrations.AlterField(
            model_name='review',
            name='content_good',
            field=models.TextField(blank=True, null=True, verbose_name='미팅 후기'),
        ),
    ]
