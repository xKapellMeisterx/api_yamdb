# Generated by Django 2.2.16 on 2022-07-17 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20220717_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]
