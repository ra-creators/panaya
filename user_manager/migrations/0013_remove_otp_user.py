# Generated by Django 3.2.10 on 2022-01-05 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0012_useraddress_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='user',
        ),
    ]