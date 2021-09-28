from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Author

from book import serializers


class BaseBookAttrViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Override the get_queryset function and specify to return objects
        for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Override the function that creates the object"""
        # Add user to the attributes of the object
        serializer.save(user=self.request.user)


class TagViewSet(BaseBookAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class AuthorViewSet(BaseBookAttrViewSet):
    """Manage authors in the database"""
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
