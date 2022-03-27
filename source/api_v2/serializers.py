from rest_framework import serializers

from webapp.models import Article


class ArticleSimpleSerializer(serializers.Serializer):
    """
    Обычный сериалайзер для модели `Article`
    """
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200,
    )

    content = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        max_length=2000,
    )

    author_id = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance


class ArticleSerializer(serializers.ModelSerializer):
    """
    Модельный сериалайзер для модели `Articles`.
    """
    class Meta:
        model = Article
        fields = ("id", "title", "content", "author_id")
        read_only_fields = ("id", "author_id")
