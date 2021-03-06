# Generated by Django 3.2.10 on 2021-12-26 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectUs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('name', models.CharField(max_length=255)),
                ('query', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'ConnectUs',
            },
        ),
        migrations.AlterModelOptions(
            name='connectemails',
            options={'verbose_name_plural': 'ConnectUsEmails'},
        ),
    ]
