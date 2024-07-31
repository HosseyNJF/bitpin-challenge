from datetime import timedelta

from constance import config
from django.core.cache import cache
from django.db import connection
from django.db.models import Count
from django.utils.timezone import now

from accounts.models import BlogUser
from blog.models import Article, Rating


class AttackMitigationService:
    @classmethod
    def _get_article_current_rate(cls, article: Article) -> float:
        cache_key = f"article:current_rate:{article.id}"
        if not (val := cache.get(cache_key)):
            interval = timedelta(minutes=config.SPIKE_PROTECTION_SAMPLING_MINUTES)
            rating_count = article.ratings.filter(modified__gt=now() - interval).aggregate(c=Count('id'))['c']
            val = rating_count / (interval.total_seconds() / 3600)
            cache.set(cache_key, val, int(interval.total_seconds() / 24))
        return val

    @classmethod
    def calculate_rating_weight(cls, rating_value: int, user: BlogUser, article: Article) -> float:
        weight = 1
        # Ignore the first rating on the article as there is no reference point to calculate weights
        if not article.rating:
            return weight

        # User reputation test
        if (
                user.date_joined > now() - timedelta(hours=config.USER_REPUTATION_MINIMUM_AGE_HOURS) or
                Rating.objects.filter(user=user).count() < config.USER_REPUTATION_MINIMUM_RATINGS
        ):
            unclamped_weight = config.USER_REPUTATION_MULTIPLIER * (6 - abs(rating_value - article.rating)) / 5
            weight *= max(0, min(1, unclamped_weight))

        # Spike protection test
        rate_threshold = article.mean_rates_per_hour + (
                config.SPIKE_PROTECTION_SAMPLING_SENSITIVITY * article.standard_deviation_rates_per_hour
        )
        if cls._get_article_current_rate(article) > rate_threshold:
            unclamped_weight = config.SPIKE_PROTECTION_MULTIPLIER * (6 - abs(rating_value - article.rating)) / 5
            weight *= max(0, min(1, unclamped_weight))

        return weight

    @classmethod
    def update_article_statistics(cls):
        start_datetime = now() - timedelta(hours=config.SPIKE_PROTECTION_ANALYSIS_INTERVAL_START_HOURS)
        end_datetime = now() - timedelta(hours=config.SPIKE_PROTECTION_ANALYSIS_INTERVAL_END_HOURS)

        with connection.cursor() as cursor:
            cursor.execute("""
                WITH cte AS (SELECT article_id, date_trunc('hour', modified) AS hour, count(id) AS rating_count
                             FROM blog_rating
                             WHERE modified >= %s AND modified < %s
                             GROUP BY article_id, date_trunc('hour', modified))
                UPDATE blog_article
                SET mean_rates_per_hour = mean, standard_deviation_rates_per_hour = sd
                FROM (SELECT 
                          article_id,
                          COALESCE(stddev(rating_count), 0) AS sd, 
                          (sum(rating_count) * 1.0 / COALESCE(NULLIF(count(distinct hour), 0), 1)) AS mean
                      FROM cte
                      GROUP by article_id) AS calc;
            """, [start_datetime, end_datetime])
