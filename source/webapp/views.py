from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse

from webapp.models import Article
from webapp.utils import article_validate


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
        new_article = Article(title=title, content=content, author=author)
        errors = article_validate(title, content, author)
        if errors:
            return render(request, 'article_create.html', {"errors": errors, "article": new_article} )
        new_article.save()
        return redirect("article_view", pk=new_article.pk)


def article_view(request, pk):
    # try:
    #     article = Article.objects.get(pk=pk)
    # except Article.DoesNotExist:
    #     raise Http404
    article = get_object_or_404(Article, pk=pk)
    context = {"article": article}
    return render(request, 'article_view.html', context)


def article_update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'article_update.html', {"article": article})
    else:
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.author = request.POST.get('author')
        errors = article_validate(article.title, article.content, article.author)
        if errors:
            return render(request, 'article_update.html', {"errors": errors, "article": article})
        article.save()
        return redirect("article_view", pk=article.pk)


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, "article_delete.html", {"article": article})
    else:
        article.delete()
        return redirect("index")
