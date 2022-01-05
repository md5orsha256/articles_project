from django import forms
from django.forms import widgets

from webapp.models import STATUS_CHOICES


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200,
                            required=True,
                            label="Название",
                            error_messages={"required": "Поле обязательно для заполнения"},
                            help_text="Введите название статьи"
                            )
    author = forms.CharField(max_length=200, required=True, label="Автор", )
    content = forms.CharField(max_length=2000, required=True, label="Описание",
                              widget=widgets.Textarea(attrs={"rows": 5, "cols": 50}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label="Статус", initial=STATUS_CHOICES[0][1])
    publish_date = forms.DateField(label="Дата публикации",
                                   widget=widgets.DateTimeInput(attrs={"type": "date"}),
                                   required=True
                                   )
