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

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Override the get_queryset function and specify to return objects
        for the current authenticated user only"""
        # Get tags from the request if it was specified
        tags = self.request.query_params.get('tags')
        # Get authors from the request if it was specified
        authors = self.request.query_params.get('authors')
        # Make copy of queryset as to not modify the original queryset
        queryset = self.queryset
        if tags:
            # Get list of ids specified
            tag_ids = self._params_to_ints(tags)
            # Filter on the foreign key object with tags__id__in
            queryset = queryset.filter(tags__id__in=tag_ids)
        if authors:
            # Get list of ids specified
            author_ids = self._params_to_ints(authors)
            # Filter by the author
            queryset = queryset.filter(authors__id__in=author_ids)

        return queryset.filter(user=self.request.user)

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
