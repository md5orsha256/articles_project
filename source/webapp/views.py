from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, RedirectView, FormView

from webapp.base import FormView as CustomFormView
from webapp.forms import ArticleForm
from webapp.models import Article


class IndexView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.order_by("updated_at")
        return render(request, 'index.html', {'articles': articles})


class ArticleCreateView(CustomFormView):
    form_class = ArticleForm
    template_name = "article_create.html"

    def form_valid(self, form):
        # tags = form.cleaned_data.pop('tags')
        # self.object = Article.objects.create(**form.cleaned_data)
        # self.object.tags.set(tags)
        self.object = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect("article_view", pk=self.object.pk)


class ArticleView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, pk=kwargs.get("pk"))
        context['article'] = article
        return context


class ArticleUpdateView(FormView):
    form_class = ArticleForm
    template_name = "article_update.html"

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super(ArticleUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        return context

    # def get_initial(self):
    #     initial = {}
    #     for key in 'title', 'content', 'author':
    #         initial[key] = getattr(self.article, key)
    #     initial['tags'] = self.article.tags.all()
    #     return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.article
        return kwargs

    def form_valid(self, form):
        # tags = form.cleaned_data.pop('tags')
        # for key, value in form.cleaned_data.items():
        #     if value is not None:
        #         setattr(self.article, key, value)
        # self.article.save()
        # self.article.tags.set(tags)
        self.article = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_view', kwargs={"pk": self.article.pk})

    def get_object(self):
        return get_object_or_404(Article, pk=self.kwargs.get("pk"))


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, "article_delete.html", {"article": article})
    else:
        article.delete()
        return redirect("index")
