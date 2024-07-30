from rest_framework import serializers

from blog.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Rating.objects.update_or_create(
            user=self.context['user'],
            article=self.context['article'],
            defaults=validated_data,
        )

    class Meta:
        model = Rating
        fields = ('value',)
