import pprint

from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api_v3.views import ArticleViewSet, LogoutView


app_name = "api_v3"


article_router = routers.DefaultRouter()
article_router.register("articles", ArticleViewSet)


urlpatterns = [
    path("", include(article_router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path("logout/", LogoutView.as_view(), name="logout")
]
