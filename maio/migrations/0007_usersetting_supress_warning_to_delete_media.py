# Generated by Django 5.1.1 on 2024-09-15 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maio', '0006_rename_usersettings_usersetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='supress_warning_to_delete_media',
            field=models.BooleanField(default=False, verbose_name='Suppress Warning to Delete MEdia'),
        ),
    ]