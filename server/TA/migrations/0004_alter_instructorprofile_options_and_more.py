# Generated by Django 4.1.13 on 2024-05-02 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TA', '0003_alter_instructorprofile_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instructorprofile',
            options={},
        ),
        migrations.AlterModelManagers(
            name='instructorprofile',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='instructorprofile',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='instructorprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='instructorprofile',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='instructorprofile',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='instructorprofile',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='instructorprofile',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='instructorprofile',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='instructorprofile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='instructorprofile',
            name='user_permissions',
        ),
        migrations.AddField(
            model_name='instructorprofile',
            name='refreshtoken',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
