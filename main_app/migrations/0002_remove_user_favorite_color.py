# Generated by Django 2.2 on 2019-06-17 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='favorite_color',
        ),
    ]
