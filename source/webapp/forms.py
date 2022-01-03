from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label="Название")
    author = forms.CharField(max_length=200, required=True, label="Автор")
    content = forms.CharField(max_length=2000, required=True, label="Автор")
