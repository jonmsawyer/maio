# Generated by Django 5.1.1 on 2024-09-19 13:20

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maio', '0019_alter_thumbnail_content_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('sort', models.IntegerField(default=0, verbose_name='Sort Order (0-9)')),
                ('name', models.CharField(default='Default Category', max_length=1024, verbose_name='Category')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maio.maiouser')),
            ],
        ),
        migrations.AddField(
            model_name='media',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='maio.category'),
        ),
    ]
