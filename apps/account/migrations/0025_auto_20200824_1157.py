# Generated by Django 3.0.8 on 2020-08-24 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_partner_real_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='real_phone',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='실제 휴대폰 번호'),
        ),
    ]
