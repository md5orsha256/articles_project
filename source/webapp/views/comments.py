from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from webapp.forms import CommentForm
from webapp.models import Comment, Article


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'comments/create.html'
    form_class = CommentForm

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.article = article
        comment.save()
        return redirect('webapp:article_view', pk=article.pk)


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'comments/update.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse("webapp:article_view", kwargs={"pk": self.object.article.pk})


class CommentDeleteView(DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("webapp:article_view", kwargs={"pk": self.object.article.pk})