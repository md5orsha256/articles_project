from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator, MaxLengthValidator
from django.db import models

from django.contrib.auth import get_user_model

# Create your models here.
from django.urls import reverse


User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Article(BaseModel):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок")
    content = models.TextField(max_length=2000, null=False, blank=False, verbose_name="Контент")
    tags = models.ManyToManyField("webapp.Tag", related_name="articles")
    author = models.ForeignKey(
        User,
        related_name="articles",
        on_delete=models.SET_DEFAULT,
        default=1,
        verbose_name="Автор",
    )

    likes = models.ManyToManyField(
        User,
        related_name="liked_articles"
    )

    def create_comment(self, author: "User", content: str) -> "Comment":

        comment = Comment(
            author=author,
            content=content,
            article=self
        )
        comment.full_clean()
        comment.save()
        Comment.objects.create
        return comment

    def get_absolute_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.pk})

    def upper(self):
        return self.title.upper()

    def __str__(self):
        return f"{self.pk}. {self.author}: {self.title}"

    class Meta:
        db_table = 'articles'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def get_avg_rating(self):
        return self.reviews.filter(is_moderated=True).aggregate(avg=models.Avg("rate")).get("avg") or 0


class Tag(BaseModel):
    name = models.CharField(max_length=30, verbose_name="Тег")

    def __str__(self):
        return f"{self.pk} - {self.name}"

    class Meta:
        db_table = 'tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Comment(BaseModel):
    content = models.TextField(
        max_length=2000,
        verbose_name="Контент",
        validators=[MaxLengthValidator(2000)]
    )

    author = models.ForeignKey(
        User,
        related_name="comments",
        default=1,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )

    article = models.ForeignKey(
        "webapp.Article",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Статья",
    )

    likes = models.ManyToManyField(
        User,
        related_name="liked_comments"
    )

    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="reviews",
    )

    article = models.ForeignKey(
        "webapp.Article",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews",
    )

    rate = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        null=False,
        blank=False,
    )

    is_moderated = models.BooleanField(default=False)

    class Meta:
        db_table = "reviews"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
