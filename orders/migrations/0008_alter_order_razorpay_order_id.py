# Generated by Django 3.2.10 on 2021-12-22 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_razorpay_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(default='nil', max_length=30),
        ),
    ]
