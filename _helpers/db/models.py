from django.db import models
from django.db.models import Manager, QuerySet
from django.utils.timezone import now


class TimeModelQuerySet(QuerySet):
    def update(self, **kwargs):
        if 'modified' not in kwargs:
            kwargs['modified'] = now()
        return super().update(**kwargs)


class TimeModelManager(Manager.from_queryset(TimeModelQuerySet)):
    def update(self, **kwargs):
        if 'modified' not in kwargs:
            kwargs['modified'] = now()
        return super().update(**kwargs)

    def bulk_create(self, objs, *args, **kwargs):
        for obj in objs:
            obj.modified = now()
        return super().bulk_create(objs, *args, **kwargs)


class TimeModel(models.Model):

    objects = TimeModelManager()

    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="زمان ساخت"
    )

    modified = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name="آخرین زمان تغییر"
    )

    class Meta:
        ordering = ('-created',)
        abstract = True
