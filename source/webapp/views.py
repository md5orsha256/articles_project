from django.shortcuts import render


from webapp.models import Article


def index_view(request):
    articles = Article.objects.order_by("updated_at")
    return render(request, 'index.html', {'articles': articles})


def create_articles_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html')
    else:
        context = {
            "title": request.POST.get('title'),
            "content": request.POST.get('content'),
            "author": request.POST.get('author'),
        }
        return render(request, 'article_view.html', context)
