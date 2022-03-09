from datetime import timedelta
from secrets import token_urlsafe

from django.contrib.auth import get_user_model
from django.utils import timezone

from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="profile",
        verbose_name="Профиль",
        on_delete=models.CASCADE,
    )

    birth_date = models.DateField(
        null=True,
        blank=False,
        verbose_name="Дата рождения",
    )

    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="avatars/",
        null=True,
        blank=False
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self) -> str:
        return f"Профиль: {self.user.username}. {self.id}"


class EmailConfirmationToken(models.Model):
    TOKEN_LIFETIME_SECONDS = 2 * 60 * 60

    token = models.CharField(null=False, max_length=255, unique=True, default=token_urlsafe)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def is_expired(self):
        return self.created_at + timedelta(seconds=self.TOKEN_LIFETIME_SECONDS) < timezone.now()
