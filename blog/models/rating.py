from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.db.models import DEFERRED

from _helpers.db.models import TimeModel
from blog.models import Article


class Rating(TimeModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='ratings',
        null=True,
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    value = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0), MaxValueValidator(5),
        ],
    )
    weight = models.FloatField(
        validators=[
            MinValueValidator(0), MaxValueValidator(1),
        ],
    )

    @classmethod
    def from_db(cls, db, field_names, values):
        instance: cls = super().from_db(db, field_names, values)
        # Store original values on model load to compare later on model save
        instance._loaded_values = dict(
            zip(field_names, (value for value in values if value is not DEFERRED))
        )
        return instance

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self._state.adding:
                self.article.total_rating_value -= self._loaded_values['value'] * self._loaded_values['weight']
                self.article.total_rating_weight -= self._loaded_values['weight']
            self.article.total_rating_value += self.value * self.weight
            self.article.total_rating_weight += self.weight
            self.article.save()
            return super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'article')
