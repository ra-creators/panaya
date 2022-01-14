# Generated by Django 3.2.10 on 2022-01-13 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_alter_product_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='products', to='product.Category'),
        ),
    ]
