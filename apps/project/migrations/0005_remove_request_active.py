# Generated by Django 2.1.1 on 2020-04-17 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_request_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='active',
        ),
    ]
