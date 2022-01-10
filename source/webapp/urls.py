from django.urls import path
from django.views.generic import RedirectView

from webapp.models import Article
from webapp.views import (
    create_article_view,
    ArticleView,
    article_update_view,
    article_delete_view, IndexView)

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('articles/', RedirectView.as_view(pattern_name="index")),
    path('articles/add/', create_article_view, name="article_add"),
    path('article/<int:pk>/', ArticleView.as_view(template_name="article_view.html"), name="article_view"),
    path('article/<int:pk>/update', article_update_view, name="article_update_view"),
    path('article/<int:pk>/delete', article_delete_view, name="article_delete_view"),
]
