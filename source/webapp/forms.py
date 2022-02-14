from django import forms
from django.core.exceptions import ValidationError

from webapp.models import Tag, Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "tags", "content")
        widgets = {
            'tags': forms.CheckboxSelectMultiple
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data['title']
        content = cleaned_data['content']
        if len(title) < 5:
            self.add_error('title', ValidationError(
                f"Значение должно быть длиннее 5 символов {title} не подходит"))
        if title == content:
            raise ValidationError("Text of the article should not duplicate it's title!")
        return cleaned_data


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)


class ArticleDeleteForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title",)

    def clean_title(self):
        if self.instance.title != self.cleaned_data.get("title"):
            raise ValidationError("Название статьи не соответствует")
        return self.cleaned_data.get("title")
