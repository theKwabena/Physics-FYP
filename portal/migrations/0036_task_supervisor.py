# Generated by Django 4.0.7 on 2022-09-15 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0035_remove_task_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='supervisor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='portal.supervisor'),
        ),
    ]
