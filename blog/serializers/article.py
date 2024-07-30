from rest_framework import serializers

from blog.models import Article


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        model = Article
        fields = ('url', 'title', 'rating')


class ArticleDetailSerializer(serializers.HyperlinkedModelSerializer):
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    rate = serializers.HyperlinkedIdentityField('article-rate')

    class Meta:
        model = Article
        fields = ('title', 'content', 'rating', 'rate')
