from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UsernameField


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")



# class MyUserCreationForm(forms.ModelForm):
#     password = forms.CharField(label="Пароль", widget=forms.PasswordInput,
#                                        strip=False)
#     password_confirm = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput,
#                                        strip=False)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_confirm = cleaned_data.get("password_confirm")
#         if password != password_confirm:
#             raise ValidationError("Пароли не совпадают")
#         return cleaned_data
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data.get("password"))
#         if commit:
#             user.save()
#         return user
#
#     class Meta:
#         model = User
#         fields = ("username", "password", "password_confirm", "email", "first_name", "last_name")
