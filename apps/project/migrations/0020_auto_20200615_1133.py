# Generated by Django 2.1.1 on 2020-06-15 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0019_auto_20200615_1130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='day_price',
            new_name='price',
        ),
    ]
