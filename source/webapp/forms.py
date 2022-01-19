from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Tag, Article


# def min_length_validator(value):
#     if len(value) < 5:
#         raise ValidationError(f"Значение должно быть длиннее 5 символов {value} не подходит")


# class ArticleForm(forms.Form):
#     title = forms.CharField(max_length=200, required=True, label="Название", validators=(min_length_validator,))
#     author = forms.CharField(max_length=200, required=True, label="Автор")
#     content = forms.CharField(max_length=2000, required=True, label="Описание",
#                               widget=widgets.Textarea(attrs={"rows": 5, "cols": 50}))
#     tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, label="Теги")


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = []
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