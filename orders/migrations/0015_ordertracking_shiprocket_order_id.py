# Generated by Django 3.2.10 on 2022-01-11 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_shiprockettoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertracking',
            name='shiprocket_order_id',
            field=models.CharField(default=456123456, max_length=20),
            preserve_default=False,
        ),
    ]
