# Generated by Django 2.1.1 on 2020-04-14 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='select',
            name='request',
            field=models.TextField(blank=True, null=True, verbose_name='선택질문'),
        ),
    ]