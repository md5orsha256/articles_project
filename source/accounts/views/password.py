from django.conf import settings
from django.contrib.auth import get_user_model, update_session_auth_hash, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, CreateView

from accounts.forms import PasswordChangeForm, ForgotPasswordForm, ResetPasswordForm
from accounts.models import Token

User = get_user_model()


class UserPasswordChangeView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_object'

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("accounts:user-profile", kwargs={"pk": self.request.user.pk})


class ForgotPasswordView(CreateView):
    template_name = "forgot_password.html"
    form_class = ForgotPasswordForm
    model = Token

    def form_valid(self, form):
        response = super(ForgotPasswordView, self).form_valid(form)

        reset_password_uri = self.request.build_absolute_uri(
            reverse("accounts:reset-password", kwargs={"token": self.object.token})
        )

        send_mail(
            "Forgot Password",
            reset_password_uri,
            settings.DEFAULT_FROM_EMAIL,
            [self.object.user.email],
            fail_silently=False
        )

        return response

    def get_success_url(self):
        return reverse("webapp:index")


class ResetPasswordView(UpdateView):
    model = User
    template_name = "reset-password.html"
    form_class = ResetPasswordForm

    def get_success_url(self):
        return reverse("accounts:user-profile", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        self._token = get_object_or_404(
            Token,
            token=self.kwargs["token"],
            type=Token.TYPE_RESET_PASSWORD
        )
        return self._token.user

    def form_valid(self, form):
        response = super().form_valid(form)
        self._token.delete()
        login(self.request, self.object)
        return response
