# Generated by Django 4.0 on 2023-10-10 11:41

import auth_app.fuctions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=auth_app.fuctions.get_timestamp_path_user, verbose_name='Аватара'),
        ),
    ]
