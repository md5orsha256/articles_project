from django.shortcuts import render, redirect, get_object_or_404

from webapp.forms import ArticleForm, ArticleDeleteForm, ArticleSearchForm
from webapp.models import Article, STATUS_CHOICES


def index_view(request):
    form = ArticleForm()
    search_value = ""
    search_form = ArticleSearchForm(data=request.GET)
    if search_form.is_valid():
        search_value = search_form.cleaned_data.get("search")
        articles = Article.objects.filter(title__contains=search_value).order_by("-created_at")
    else:
        articles = Article.objects.order_by("-created_at")
    return render(request, 'index.html', {'articles': articles,
                                          "statuses": STATUS_CHOICES,
                                          "create_form": form,
                                          "search_form": search_form,
                                          "search_value": search_value})


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
            new_article = form.save()
            return redirect("article_view", pk=new_article.pk)
        if "add" in request.META.get("HTTP_REFERER"):
            return render(request, 'article_create.html', {"form": form})
        search_value = request.POST.get("search")
        search_form = ArticleSearchForm(initial={
            "search": search_value
        })
        articles = Article.objects.filter(title__contains=search_value).order_by("-created_at")
        return render(request, 'index.html', {"create_form": form,
                                              'articles': articles,
                                              "search_form": search_form,
                                              "statuses": STATUS_CHOICES})


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
