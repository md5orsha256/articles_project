from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.mail import send_mail
from django.conf import settings

from accounts.models import Profile, Token

User = get_user_model()


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "birth_date")


class ResetPasswordForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ('password', 'password_confirm')


class PasswordChangeForm(ResetPasswordForm):
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    class Meta:
        model = User
        fields = ('password', 'password_confirm', 'old_password')


class ForgotPasswordForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Token
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        try:
            self._user = User.objects.get(
                email=email
            )
        except User.DoesNotExist:
            raise forms.ValidationError(
                "User does not exists",
                code="invalid"
            )

        return email

    def save(self):
        return Token.create_reset_password(self._user)
