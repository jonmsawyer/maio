# Generated by Django 5.1.1 on 2024-09-15 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maio', '0005_usersettings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserSettings',
            new_name='UserSetting',
        ),
    ]
