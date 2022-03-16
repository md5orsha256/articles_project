from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from accounts.forms import MyUserCreationForm
from accounts.models import Profile, Token


User = get_user_model()


class RegisterView(CreateView):
    model = User
    template_name = "registration.html"
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        Profile.objects.create(user=user)

        token = Token.create_email_confirmation(user)

        confirm_email_url = self.request.build_absolute_uri(
            reverse("accounts:confirm-email", kwargs={"token": token.token})
        )

        send_mail(
            'Подтверждение адреса электронной почты',
            f'Перейдите по ссылке {confirm_email_url}, чтобы подтвердить адрес электронной почты',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url



class EmailConfirmView(View):
    def get(self, request, *args, **kwargs):
        email_confirm_token = kwargs.get("token")
        token = get_object_or_404(Token, token=email_confirm_token)

        if token.is_expired():
            return HttpResponseBadRequest(b"Token is expired")

        user = token.user
        user.is_active = True
        user.save()
        token.delete()

        login(request, user)

        redirect_to = reverse("webapp:index")
        return HttpResponseRedirect(redirect_to=redirect_to)
