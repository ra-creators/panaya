# Generated by Django 3.2.10 on 2021-12-18 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_faq_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='question',
            field=models.TextField(),
        ),
    ]
