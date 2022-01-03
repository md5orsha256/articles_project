from django.shortcuts import render, redirect, get_object_or_404

from webapp.forms import ArticleForm
from webapp.models import Article


def index_view(request):
    articles = Article.objects.order_by("updated_at")
    return render(request, 'index.html', {'articles': articles})


def create_article_view(request):
    if request.method == 'GET':
        form = ArticleForm()
        return render(request, 'article_create.html', {"form": form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            author = form.cleaned_data.get('author')
            new_article = Article.objects.create(title=title, content=content, author=author)
            return redirect("article_view", pk=new_article.pk)
        return render(request, 'article_create.html', {"form": form})


def article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {"article": article}
    return render(request, 'article_view.html', context)


def article_update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        form = ArticleForm(initial={
            'title': article.title,
            'content': article.content,
            'author': article.author
        })
        return render(request, 'article_update.html', {"article": article, "form": form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = request.POST.get('title')
            article.content = request.POST.get('content')
            article.author = request.POST.get('author')
            article.save()
            return redirect("article_view", pk=article.pk)
        return render(request, 'article_update.html', {"article": article, "form": form})


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, "article_delete.html", {"article": article})
    else:
        article.delete()
        return redirect("index")
