# Generated by Django 5.0.9 on 2024-09-26 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maio', '0033_alter_libraryshare_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='maiomap',
            options={'get_latest_by': ['-date_modified'], 'ordering': ['-date_modified'], 'verbose_name': 'Maio Map', 'verbose_name_plural': 'Maio Map'},
        ),
        migrations.AlterModelTableComment(
            name='maiomap',
            table_comment='Maio Map maps types to values.',
        ),
        migrations.RenameField(
            model_name='maiomap',
            old_name='ins_dttm',
            new_name='date_added',
        ),
        migrations.RenameField(
            model_name='maiomap',
            old_name='upd_dttm',
            new_name='date_modified',
        ),
    ]
