from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from blog.models import Article
from blog.serializers import ArticleSerializer, ArticleDetailSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return ArticleSerializer
            case 'retrieve':
                return ArticleDetailSerializer

        raise NotImplementedError
