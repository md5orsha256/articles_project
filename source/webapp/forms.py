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

    def clean_title(self):
        if len(self.cleaned_data.get('title')) < 5:
            raise ValidationError(f"Значение должно быть длиннее 5 символов {self.cleaned_data.get('title')} не подходит")
        return self.cleaned_data.get('title')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['content'] == cleaned_data['title']:
            raise ValidationError("Text of the article should not duplicate it's title!")
        return cleaned_data