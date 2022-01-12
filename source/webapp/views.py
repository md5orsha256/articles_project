from django.shortcuts import render, redirect, get_object_or_404

from webapp.forms import ArticleForm, ArticleDeleteForm
from webapp.models import Article, STATUS_CHOICES


def index_view(request):
    form = ArticleForm()
    articles = Article.objects.filter().order_by("-created_at")
    return render(request, 'index.html', {'articles': articles, "statuses": STATUS_CHOICES, "form": form})


def index_status_view(request, status):
    status_name = dict(STATUS_CHOICES)[status]
    articles = Article.objects.filter(status=status).order_by("title")
    return render(request, 'index_status.html', {'articles': articles, "status": status_name})


def create_article_view(request):
    if request.method == 'GET':
        form = ArticleForm()
        return render(request, 'article_create.html', {"form": form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            # new_article = form.save() с модельной формой создать статью можно так
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
        form = ArticleDeleteForm()
        return render(request, "article_delete.html", {"article": article, "form": form})
    else:
        form = ArticleDeleteForm(data=request.POST)
        if form.is_valid():
            if form.cleaned_data.get("title") != article.title:
                form.errors['title'] = ["Название статьи не соответствует"]
                return render(request, "article_delete.html", {"article": article, "form": form})
            article.delete()
            return redirect("index")
        return render(request, "article_delete.html", {"article": article, "form": form})
