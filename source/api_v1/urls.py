from django.urls import path, include

from api_v1.views import echo_view, get_csrf_token_view, article_list_view


app_name = "api_v1"


articles_urlpatterns = [
    path("", article_list_view, name="article_list"),
]


urlpatterns = [
    path("echo/", echo_view),
    path("get-csrf-token/", get_csrf_token_view),
    path("articles/", include(articles_urlpatterns)),
]
