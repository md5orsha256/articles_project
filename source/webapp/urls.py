from django.urls import path

from webapp.views import index_view, create_article_view, article_view, article_update_view

urlpatterns = [
    path('', index_view, name="index"),
    path('articles/add/', create_article_view, name="article_add"),
    path('article/<int:pk>/', article_view, name="article_view"),
    path('article/<int:pk>/update', article_update_view, name="article_update_view")
]