# Generated by Django 3.0 on 2023-12-25 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='uid',
        ),
    ]
