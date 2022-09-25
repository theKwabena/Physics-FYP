# Generated by Django 4.1 on 2022-08-29 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0015_project_occupied'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('deadline', models.DateTimeField()),
                ('project_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.project')),
            ],
        ),
    ]
