# Generated by Django 3.2.10 on 2021-12-18 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_faq_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(),
        ),
    ]
