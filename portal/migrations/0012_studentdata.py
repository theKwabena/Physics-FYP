# Generated by Django 4.1 on 2022-08-15 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0011_project_selected'),
    ]

    operations = [
        migrations.CreateModel(
            name='studentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='')),
                ('migrated', models.BooleanField(default=False)),
            ],
        ),
    ]
