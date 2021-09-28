from rest_framework import serializers

from core.models import Tag, Author, Book


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for author objects"""

    class Meta:
        model = Author
        fields = ('id', 'name')
        read_only_fields = ('id',)


class BookSerializer(serializers.ModelSerializer):
    """Serialize a book"""
    authors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Author.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Book
        fields = (
            'id', 'title', 'pages', 'year', 'tags', 'authors',
            'price', 'link'
        )
        read_only_fields = ('id',)


class BookDetailSerializer(BookSerializer):
    """Serialize a book detail"""
    # Serialize the author attribute with the Author serializer
    authors = AuthorSerializer(many=True, read_only=True)
    # Serialize the tag attribute with the Tag serializer
    tags = TagSerializer(many=True, read_only=True)


class BookImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to books"""

    class Meta:
        model = Book
        fields = ('id', 'image')
        read_only_fields = ('id',)
