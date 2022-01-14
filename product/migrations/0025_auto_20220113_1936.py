# Generated by Django 3.2.10 on 2022-01-13 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_auto_20220113_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('value', models.CharField(max_length=10, verbose_name='color value eg. #FFF')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(blank=True, related_name='products', to='product.Color'),
        ),
    ]
