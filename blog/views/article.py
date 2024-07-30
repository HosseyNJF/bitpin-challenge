from django.db.models import Avg, Subquery
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from blog.models import Article, Rating
from blog.serializers import ArticleSerializer, ArticleDetailSerializer, RatingSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Article.objects.all().annotate(
            rating=Avg('ratings__value'),
            your_rating=Subquery(
                Rating.objects.filter(user=self.request.user).values('value')
            )
        )

    def get_serializer_class(self):
        match self.action:
            case 'rate':
                return RatingSerializer
            case 'list':
                return ArticleSerializer
            case 'retrieve':
                return ArticleDetailSerializer

        raise NotImplementedError

    def get_serializer_context(self):
        if self.action == 'rate':
            return {
                'article': self.get_object(),
                'user': self.request.user,
            }
        return super().get_serializer_context()

    @action(detail=True, methods=['post'])
    def rate(self, request: Request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
