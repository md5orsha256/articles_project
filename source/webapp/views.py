from django.shortcuts import render


# Create your views here.

def index_view(request):
    print(request.GET.getlist("title", "Vasya Pupkin"))
    # context = {"name":"Vasya", "title": "lalala"}
    return render(request, 'index.html', {"name": "Vasya", "title": "lalala"})


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
