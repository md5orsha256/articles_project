import json
from datetime import datetime
from http import HTTPStatus

from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed

from webapp.models import Article


@ensure_csrf_cookie
def get_csrf_token_view(request):
    if request.method == "GET":
        return HttpResponse()
    return HttpResponseNotAllowed(["GET"])


def echo_view(request):
    response_data = {
        "method": request.method,
        "datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    print(request.body)
    if request.body:
        response_data["body"] = json.loads(request.body)

    response = JsonResponse(response_data)

    return response


def article_list_view(request):
    if request.method == "GET":
        response_article_fields = ["pk", "title", "content", "author_id"]
        articles = Article.objects.all().values(*response_article_fields)

        return JsonResponse(list(articles), safe=False)

    elif request.method == "POST":
        article_data = json.loads(request.body)
        article = Article.objects.create(**article_data)

        return JsonResponse(
            {
                "pk": article.pk,
                "title": article.title,
                "content": article.content,
            },
            status=HTTPStatus.CREATED
        )

    return HttpResponseNotAllowed(["GET", "POST"])
