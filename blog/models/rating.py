from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from _helpers.db.models import TimeModel
from blog.models import Article


class Rating(TimeModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings',
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

    class Meta:
        unique_together = ('user', 'article')
