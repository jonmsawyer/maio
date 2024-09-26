# Generated by Django 5.1.1 on 2024-09-26 00:13

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maio', '0031_usersetting_display_debug'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryShare',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('permission', models.CharField(choices=[('denied', 'Denied'), ('create', 'Create'), ('read', 'Read'), ('update', 'Update'), ('delete', 'Delete')], default='denied', verbose_name='Permissions')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date Modified')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='maio.maiouser', verbose_name='From Maio User')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='maio.maiouser', verbose_name='To Maio User')),
            ],
            options={
                'verbose_name': 'User Setting',
                'verbose_name_plural': 'User Settings',
                'db_table_comment': 'User system-wide settings.',
                'ordering': ['-date_modified'],
                'get_latest_by': ['-date_modified'],
                'unique_together': {('from_user', 'to_user')},
            },
        ),
    ]