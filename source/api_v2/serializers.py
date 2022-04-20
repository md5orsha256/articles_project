import json

from rest_framework import serializers

from webapp.models import Article, Tag


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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name", "id")


class MySuperSerializer(serializers.Serializer):
    a = serializers.IntegerField(required=True)
    b = serializers.CharField(max_length=120)


class ArticleSerializer(serializers.ModelSerializer):
    """
    Модельный сериалайзер для модели `Articles`.
    """

    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        source="tags",
        many=True,
        queryset=Tag.objects.all(),
        write_only=True
    )

    super_data = MySuperSerializer(many=True, write_only=True)

    class Meta:
        model = Article
        fields = ("id", "title", "content", "author_id", "tags", "tag_ids", "super_data")
        read_only_fields = ("id", "author_id")

    def save(self, **kwargs):
        print(self.validated_data)
        with open("my_awesome_file.json", "w") as f:
            json.dump(self.validated_data.pop("super_data"), f)

        return super(ArticleSerializer, self).save()
