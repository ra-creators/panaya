# Generated by Django 3.2.10 on 2021-12-21 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0007_alter_useraddress_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
