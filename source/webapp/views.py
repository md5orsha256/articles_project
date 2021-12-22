from django.shortcuts import render

from webapp.models import Article, STATUS_CHOICES


def index_view(request):
    if request.GET.get("is_admin", "0") == "1":
        articles = Article.objects.order_by("updated_at")
    else:
        articles = Article.objects.filter(status='moderated').order_by("updated_at")
    return render(request, 'index.html', {'articles': articles})


def create_article_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html', {"status_choices": STATUS_CHOICES})
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        status = request.POST.get('status')
        new_article = Article.objects.create(title=title,
                                             content=content,
                                             author=author,
                                             status=status)
        context = {"article": new_article}

        return render(request, 'article_view.html', context)


def article_view(request):
    pk = request.GET.get("pk")
    article = Article.objects.get(pk=pk)
    context = {"article": article}
    return render(request, 'article_view.html', context)
