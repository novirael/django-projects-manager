# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now, blank=True)),
                ('finish_date', models.DateField(null=True, blank=True)),
                ('sum_hours_work', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('link_repository', models.URLField(max_length=256, blank=True)),
                ('trello_id', models.CharField(max_length=32, blank=True)),
                ('trello_url', models.URLField(max_length=256, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('time', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('trello_id', models.CharField(max_length=32, blank=True)),
                ('trello_url', models.URLField(max_length=256, blank=True)),
                ('trello_last_activity', models.DateTimeField(null=True, blank=True)),
                ('project', models.ForeignKey(related_name='tasks', to='tasks_manager.Project')),
            ],
            options={
                'ordering': ['-trello_last_activity'],
            },
        ),
    ]
