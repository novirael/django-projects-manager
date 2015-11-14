import os
import logging

from django.db import models
from django.utils import timezone

from trello import TrelloClient

logger = logging.getLogger(__name__)


TRELLO_KEYS = {
    'api_key': os.environ.get('TRELLO_API'),
    'api_secret': os.environ.get('TRELLO_API_SECRET'),
    'token': os.environ.get('TRELLO_TOKEN'),
    'token_secret': os.environ.get('TRELLO_TOKEN_SECRET'),
}


class NotSetTrelloBoardID(Exception):
    pass


class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    start_date = models.DateField(blank=True, default=timezone.now)
    finish_date = models.DateField(blank=True, null=True)
    sum_hours_work = models.DecimalField(
        max_digits=6, decimal_places=2, default=0
    )
    link_repository = models.URLField(max_length=256, blank=True)

    trello_id = models.CharField(max_length=32, blank=True)
    trello_url = models.URLField(max_length=256, blank=True)

    def __unicode__(self):
        return self.name

    @property
    def total_time(self):
        time = 0
        for task in self.tasks.all():
            time += task.time
        return time

    def sync_trello_cards(self):
        if not self.trello_id:
            logger.exception("Trello board id for %s not set", self.name)
            raise NotSetTrelloBoardID

        client = TrelloClient(**TRELLO_KEYS)
        tasks = client.fetch_json("boards/{}/cards".format(self.trello_id))

        for task_dict in tasks:
            last_activity = task_dict.get('dateLastActivity')
            task, created = Task.objects.get_or_create(
                trello_id=task_dict['id'],
                project=self
            )
            if created or last_activity != task.trello_last_activity:
                task.name = task_dict['name']
                task.description = task_dict['desc']
                task.trello_url = task_dict['shortUrl']
                task.trello_last_activity = last_activity
                task.save()

                logger.info(
                    "Trello card with id %s and name %s has ben %s",
                    task_dict['id'],
                    task_dict['name'],
                    'created' if created else 'updated'
                )


class Task(models.Model):
    project = models.ForeignKey(Project, related_name="tasks")
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    time = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True, blank=True)

    trello_id = models.CharField(max_length=32, blank=True)
    trello_url = models.URLField(max_length=256, blank=True)
    trello_last_activity = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-trello_last_activity']
