from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ArticleForm, ArticleDeleteForm
from webapp.models import Article
from webapp.views.base import SearchView


class IndexView(SearchView):
    model = Article
    context_object_name = "articles"
    template_name = "articles/index.html"
    paginate_by = 3
    paginate_orphans = 0
    search_fields = ["title__icontains", "author__icontains"]
    ordering=["-updated_at"]


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/create.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect("accounts:login")


class ArticleView(DetailView):
    template_name = 'articles/view.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.order_by("-created_at")
        context['comments'] = comments
        return context


class ArticleUpdateView(UpdateView):
    form_class = ArticleForm
    template_name = "articles/update.html"
    model = Article


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "articles/delete.html"
    success_url = reverse_lazy('webapp:index')
    form_class = ArticleDeleteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs['instance'] = self.object
        return kwargs