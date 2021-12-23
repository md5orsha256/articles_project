from django.shortcuts import render
from django.http import HttpResponseRedirect

from webapp.models import Article


def index_view(request):
    articles = Article.objects.order_by("updated_at")
    return render(request, 'index.html', {'articles': articles})


def create_article_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html')
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        new_article = Article.objects.create(title=title, content=content, author=author)
        # context = {"article": new_article}
        return HttpResponseRedirect(f"/article/{new_article.pk}")
        # return render(request, 'article_view.html', context)


def article_view(request, pk):
    # pk = request.GET.get("pk")
    article = Article.objects.get(pk=pk)
    context = {"article": article}
    return render(request, 'article_view.html', context)
