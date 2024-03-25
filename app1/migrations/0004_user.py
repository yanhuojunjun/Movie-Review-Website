# Generated by Django 3.0 on 2023-12-25 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app1', '0003_delete_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('gender', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]