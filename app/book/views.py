from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Author, Book

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


class BookViewSet(viewsets.ModelViewSet):
    """Manage books in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        """Override the get_queryset function and specify to return objects
        for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.BookDetailSerializer
        elif self.action == 'upload_image':
            return serializers.BookImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new book"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a book"""
        book = self.get_object()
        serializer = self.get_serializer(
            book,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
