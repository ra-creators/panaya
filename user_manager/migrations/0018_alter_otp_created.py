# Generated by Django 3.2.10 on 2022-01-05 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0017_otp_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
