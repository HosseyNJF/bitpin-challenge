from rest_framework import generics
from rest_framework.permissions import AllowAny

from accounts.models import BlogUser
from accounts.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = BlogUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
