# Generated by Django 2.1.1 on 2020-04-09 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_partner_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='phone',
        ),
    ]
