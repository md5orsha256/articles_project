from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import TemplateView, FormView, ListView

from webapp.base import FormView as CustomFormView, ListView as CustomListView
from webapp.forms import ArticleForm, SearchForm
from webapp.models import Article


class IndexView(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "index.html"
    paginate_by = 3
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            print(self.search_value)
            query = Q(title__icontains=self.search_value) | Q(author__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by("-updated_at")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = SearchForm()
        if self.search_value:
            context['search'] = self.search_value
        return context

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")



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
