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
            status = form.cleaned_data.get('status')
            publish_date = form.cleaned_data.get('publish_date')
            new_article = Article.objects.create(title=title,
                                                 content=content,
                                                 author=author,
                                                 status=status,
                                                 publish_date=publish_date)
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
            'author': article.author,
            "status": article.status,
            "publish_date": article.publish_date.strftime('%Y-%m-%d')
        })
        return render(request, 'article_update.html', {"article": article, "form": form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data.get('title')
            article.content = form.cleaned_data.get('content')
            article.author = form.cleaned_data.get('author')
            article.status = form.cleaned_data.get('status')
            article.publish_date = form.cleaned_data.get('publish_date')
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
