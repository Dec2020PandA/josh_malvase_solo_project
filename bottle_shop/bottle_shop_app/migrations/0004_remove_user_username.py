# Generated by Django 2.2 on 2020-12-11 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bottle_shop_app', '0003_user_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
