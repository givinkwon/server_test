# Generated by Django 2.1.1 on 2020-03-30 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paylist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_uid', models.CharField(max_length=256, verbose_name='결제정보')),
                ('buyer_email', models.CharField(max_length=256, verbose_name='구매자 이메일')),
                ('buyer_name', models.CharField(max_length=256, verbose_name='구매자 이름')),
                ('buyer_tel', models.CharField(max_length=256, verbose_name='구매자 전화번호')),
                ('state', models.IntegerField(choices=[(0, '결제 실패'), (1, '결제 성공')], default=0, verbose_name='결제 상태')),
            ],
            options={
                'verbose_name': '     결제저장',
                'verbose_name_plural': '     결제저장',
            },
        ),
    ]
