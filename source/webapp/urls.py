from django.urls import path
from django.views.generic import RedirectView

from webapp.views import (
    ArticleCreateView,
    ArticleView,
    ArticleUpdateView,
    article_delete_view, IndexView)

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('articles/', RedirectView.as_view(pattern_name="index")),
    path('articles/add/', ArticleCreateView.as_view(), name="article_add"),
    path('article/<int:pk>/', ArticleView.as_view(template_name="articles/view.html"), name="article_view"),
    path('article/<int:pk>/update', ArticleUpdateView.as_view(), name="article_update_view"),
    path('article/<int:pk>/delete', article_delete_view, name="article_delete_view"),
]
