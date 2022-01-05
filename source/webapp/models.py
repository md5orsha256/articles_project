from django.db import models

# Create your models here.
STATUS_CHOICES = [('new', 'Новая'), ('moderated', 'Модерирована'), ('rejected', 'Откланена')]


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок")
    author = models.CharField(max_length=200, null=False, blank=False, verbose_name="Автор", default="Unknown")
    content = models.TextField(max_length=2000, null=False, blank=False, verbose_name="Контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    status = models.CharField(max_length=15, default='new', choices=STATUS_CHOICES, verbose_name="Статус")

    def __str__(self):
        return f"{self.pk}. {self.author}: {self.title}"

    class Meta:
        db_table = 'articles'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
