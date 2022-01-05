from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import STATUS_CHOICES, Article
from datetime import date


# def publish_date_validate(value):
#     if value < date.today():
#         raise ValidationError("дата публикации не может быть раньше чем сегодня")

# class ArticleForm(forms.Form):
#     title = forms.CharField(max_length=200,
#                             required=True,
#                             label="Название",
#                             error_messages={"required": "Поле обязательно для заполнения"},
#                             help_text="Введите название статьи"
#                             )
#     author = forms.CharField(max_length=200, required=True, label="Автор", )
#     content = forms.CharField(max_length=2000, required=True, label="Описание",
#                               widget=widgets.Textarea(attrs={"rows": 5, "cols": 50}))
#     status = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label="Статус", initial=STATUS_CHOICES[0][1])
#     publish_date = forms.DateField(label="Дата публикации",
#                                    widget=widgets.DateTimeInput(attrs={"type": "date"}),
#                                    required=True
#                                    )
#     def clean_publish_date(self):
#         if self.cleaned_data.get("publish_date") < date.today():
#             raise ValidationError("дата публикации не может быть раньше чем сегодня")
#         return self.cleaned_data.get("publish_date")
#
#     def clean(self):
#         return self.cleaned_data

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        error_messages = {
            "title": {
                "required": "Поле обязательно для заполнения"
            }
        }
        help_texts = {
            "title": "Введите заголовок"
        }
        widgets = {
            "publish_date": widgets.DateTimeInput(attrs={"type": "date"})
        }


class ArticleDeleteForm(forms.Form):
    title = forms.CharField(max_length=200,
                            required=True,
                            label="Название",
                            error_messages={"required": "Поле обязательно для заполнения"},
                            )
