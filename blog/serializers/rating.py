from rest_framework import serializers

from blog.models import Rating
from blog.services import AttackMitigationService


class RatingSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Rating.objects.update_or_create(
            user=self.context['user'],
            article=self.context['article'],
            defaults={
                **validated_data,
                'weight': AttackMitigationService.calculate_rating_weight(
                    validated_data['value'], self.context['user'], self.context['article'],
                )
            },
        )

    class Meta:
        model = Rating
        fields = ('value',)
