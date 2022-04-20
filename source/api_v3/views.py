from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS, AllowAny

from api_v2.serializers import ArticleSerializer
from webapp.models import Article


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(status=204)


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = (IsAuthenticated,)

    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         return [AllowAny()]
    #     return [IsAdminUser()]
