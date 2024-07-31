from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'rating')
    search_fields = ('id', 'title', 'content')
    exclude = ('total_rating_value', 'total_rating_weight', 'mean_rates_per_hour', 'standard_deviation_rates_per_hour')
