# Generated by Django 3.2.10 on 2021-12-17 13:25

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_created=True)),
                ('title', models.CharField(default='Title', max_length=100)),
                ('author', models.CharField(default='admin', max_length=100)),
                ('image', models.FileField(upload_to='blogs/')),
                ('content', ckeditor.fields.RichTextField()),
                ('likes', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', ckeditor.fields.RichTextField()),
                ('mail', models.EmailField(max_length=254)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.blog')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
