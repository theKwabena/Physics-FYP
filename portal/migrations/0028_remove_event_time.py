# Generated by Django 4.0.7 on 2022-09-11 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0027_pitchedtopic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='time',
        ),
    ]
