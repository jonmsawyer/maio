# Generated by Django 5.0.9 on 2024-10-19 00:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maio', '0035_alter_caption_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metafile',
            name='content_file',
            field=models.FileField(max_length=1024, upload_to='E:\\Django\\maio\\filestore\\meta', verbose_name='Meta File'),
        ),
        migrations.CreateModel(
            name='Converted',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('content_file', models.FileField(max_length=1024, upload_to='E:\\Django\\maio\\filestore\\converted', verbose_name='Content File')),
                ('size', models.PositiveIntegerField(verbose_name='Size (Bytes)')),
                ('width', models.PositiveIntegerField(verbose_name='Width (Pixels)')),
                ('height', models.PositiveIntegerField(verbose_name='Height (Pixels)')),
                ('length', models.DecimalField(decimal_places=15, max_digits=22, verbose_name='Length (seconds)')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date Modified')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maio.file')),
                ('mime_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='maio.maiomimetype')),
            ],
            options={
                'verbose_name': 'Converted File',
                'verbose_name_plural': 'Converted Files',
                'db_table_comment': 'Converted Files.',
                'ordering': ['-date_modified'],
                'get_latest_by': ['-date_modified'],
            },
        ),
    ]
