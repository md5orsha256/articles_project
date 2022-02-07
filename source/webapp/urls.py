from django.urls import path
from django.views.generic import RedirectView

from webapp.views import (
    ArticleCreateView,
    ArticleView,
    ArticleUpdateView,
    ArticleDeleteView, IndexView, CommentCreateView, CommentUpdateView, CommentDeleteView)

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('articles/', RedirectView.as_view(pattern_name="index")),
    path('articles/add/', ArticleCreateView.as_view(), name="article_add"),
    path('article/<int:pk>/', ArticleView.as_view(template_name="articles/view.html"), name="article_view"),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name="article_update_view"),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name="article_delete_view"),
    path('article/<int:pk>/comments/add/', CommentCreateView.as_view(), name="article_comment_create"),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name="comment_update_view"),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name="comment_delete_view"),
]
