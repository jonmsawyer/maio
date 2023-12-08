# Generated by Django 2.0.3 on 2018-04-16 01:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import maio.models.maiofields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Caption',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=1024)),
                ('url', models.URLField(blank=True, max_length=1024, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('caption_date', models.DateTimeField(blank=True, null=True)),
                ('caption', models.TextField()),
            ],
            options={
                'ordering': ['caption_date'],
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('md5sum', maio.models.maiofields.FixedCharField(max_length=32, unique=True)),
                ('original_name', models.CharField(max_length=1024)),
                ('original_extension', models.CharField(blank=True, max_length=8, null=True)),
                ('mime_type', models.CharField(max_length=64)),
                ('size', models.PositiveIntegerField(default=0)),
                ('mtime', models.FloatField(default=0.0)),
                ('tn_path', models.CharField(max_length=1024)),
                ('file_path', models.CharField(max_length=1024)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField()),
            ],
            options={
                'ordering': ['-date_modified'],
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('document', 'Document'), ('other', 'Other')], max_length=8)),
                ('name', models.CharField(max_length=1024)),
                ('extension', models.CharField(blank=True, max_length=8, null=True)),
                ('mtime', models.FloatField(default=0.0)),
                ('size', models.PositiveIntegerField(default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField()),
                ('width', models.PositiveIntegerField(blank=True, null=True)),
                ('height', models.PositiveIntegerField(blank=True, null=True)),
                ('tn_width', models.PositiveIntegerField(blank=True, null=True)),
                ('tn_height', models.PositiveIntegerField(blank=True, null=True)),
                ('length', models.FloatField(blank=True, null=True)),
                ('is_loved', models.BooleanField(default=False)),
                ('is_liked', models.BooleanField(default=False)),
                ('rating', models.PositiveSmallIntegerField(default=0)),
                ('author', models.CharField(blank=True, max_length=1024, null=True)),
                ('url', models.URLField(blank=True, max_length=1024, null=True)),
                ('source', models.CharField(blank=True, max_length=1024, null=True)),
                ('copyright', models.CharField(blank=True, max_length=128, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_hidden', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maio.File')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_modified'],
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('tn_path', models.CharField(max_length=1024)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('default_order', models.PositiveSmallIntegerField(default=0)),
                ('seconds_between', models.FloatField(default=5.0)),
                ('caption', models.TextField(blank=True, null=True)),
                ('media', models.ManyToManyField(to='maio.Media')),
            ],
            options={
                'ordering': ['-date_modified'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='media',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='maio.Tag'),
        ),
        migrations.AddField(
            model_name='caption',
            name='media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maio.Media'),
        ),
    ]
