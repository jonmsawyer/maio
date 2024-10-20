# Generated by Django 5.0.9 on 2024-10-20 11:54

import maio.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maio', '0041_love_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Like',
            new_name='Bookmark',
        ),
        migrations.AlterModelOptions(
            name='bookmark',
            options={'get_latest_by': ['-date_modified'], 'ordering': ['-date_modified'], 'verbose_name': 'Bookmark', 'verbose_name_plural': 'Bookmarks'},
        ),
        migrations.AlterModelTableComment(
            name='bookmark',
            table_comment='Contains the Bookmarks for Media.',
        ),
        migrations.AlterModelTableComment(
            name='rating',
            table_comment='Contains the Ratings for Media.',
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0, validators=[maio.validators.validate_rating], verbose_name='Rating'),
        ),
    ]
