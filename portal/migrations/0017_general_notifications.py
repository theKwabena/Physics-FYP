# Generated by Django 4.1 on 2022-09-02 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0016_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='General_Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(1, 'Supervisors'), (2, 'Students'), (3, 'All')], max_length=255)),
                ('message', models.TextField()),
            ],
        ),
    ]
