# Generated by Django 5.1.1 on 2024-09-15 08:18

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maio', '0001_squashed_0004_filestat'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
                ('display_thumbnails_only', models.BooleanField(default=False, verbose_name='Display Thumbnails Only')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maio.maiouser', verbose_name='Maio User')),
            ],
        ),
    ]
