# Generated by Django 4.0.1 on 2022-01-23 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_urls', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='link',
            options={'ordering': ('-date_created',)},
        ),
    ]
