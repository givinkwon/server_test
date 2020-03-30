# Generated by Django 2.1.1 on 2020-03-30 04:59

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='제목')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='내용')),
                ('is_top', models.BooleanField(default=False, verbose_name='상단고정여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일자')),
                ('link', models.CharField(max_length=300, verbose_name='링크')),
            ],
            options={
                'verbose_name': '   매거진',
                'verbose_name_plural': '   매거진',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='제목')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='내용')),
                ('is_top', models.BooleanField(default=False, verbose_name='상단고정여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일자')),
            ],
            options={
                'verbose_name': '   게시글',
                'verbose_name_plural': '   게시글',
            },
        ),
    ]
