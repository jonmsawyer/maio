# Generated by Django 2.0.3 on 2018-04-16 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='tags',
            field=models.ManyToManyField(to='maio.Tag'),
        ),
    ]
