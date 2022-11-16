from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework import filters

from .models import User
#from .permissions import IsAuthorOrReadOnly
from .serializers import UserSerializer, UserMeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    # permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly, ]


class UserMeViewSet(
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
    ):
    serializer_class = UserMeSerializer

    def get_queryset(self):
        queryset = get_object_or_404(User, username=self.request.user.username)
        return queryset