# Generated by Django 4.0.7 on 2022-09-15 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0029_remove_supervisor_iscoordinator_supervisor_role_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supervisor',
            old_name='last_name',
            new_name='other_names',
        ),
    ]
