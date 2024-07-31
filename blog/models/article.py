from django.db import models

from _helpers.db.models import TimeModel


class Article(TimeModel):
    title = models.CharField(max_length=1024, unique=True)
    content = models.TextField()

    total_rating_value = models.FloatField(default=0)
    total_rating_weight = models.FloatField(default=0)

    @property
    def rating(self):
        if not self.total_rating_weight:
            return None
        return self.total_rating_value / self.total_rating_weight

    mean_rates_per_hour = models.FloatField(default=0)
    standard_deviation_rates_per_hour = models.FloatField(default=0)
