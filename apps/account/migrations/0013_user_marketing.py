# Generated by Django 2.1.1 on 2020-06-01 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_partner_is_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='marketing',
            field=models.BooleanField(default=True, null=True, verbose_name='마케팅동의여부'),
        ),
    ]
