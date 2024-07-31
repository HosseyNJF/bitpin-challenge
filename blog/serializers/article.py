from rest_framework import serializers

from blog.models import Article


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    your_rating = serializers.IntegerField()

    class Meta:
        model = Article
        fields = ('url', 'title', 'rating', 'your_rating')


class ArticleDetailSerializer(serializers.HyperlinkedModelSerializer):
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    your_rating = serializers.IntegerField()
    rate_url = serializers.HyperlinkedIdentityField('article-rate')

    class Meta:
        model = Article
        fields = ('title', 'content', 'rating', 'your_rating', 'rate_url')
