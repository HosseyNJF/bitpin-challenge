from django.db import models

from _helpers.db.models import TimeModel


class Article(TimeModel):
    title = models.CharField(max_length=1024, unique=True)
    content = models.TextField()
