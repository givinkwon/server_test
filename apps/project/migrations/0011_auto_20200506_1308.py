# Generated by Django 2.1.1 on 2020-05-06 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20200420_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='expert',
            field=models.TextField(blank=True, null=True, verbose_name='전문성 및 경험'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='strategy',
            field=models.TextField(blank=True, null=True, verbose_name='제안 전략'),
        ),
    ]