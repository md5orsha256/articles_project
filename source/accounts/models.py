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


class Token(models.Model):
    TOKEN_LIFETIME_SECONDS = 2 * 60 * 60

    TYPE_EMAIL_CONFORMATION = "email-confirmation"
    TYPE_RESET_PASSWORD = "reset-password"
    TYPES = (
        (TYPE_EMAIL_CONFORMATION, "Email confirmation"),
        (TYPE_RESET_PASSWORD, "Reset password"),
    )

    token = models.CharField(null=False, max_length=255, unique=True, default=token_urlsafe)
    type = models.CharField(null=False, max_length=255, choices=TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tokens"

    def is_expired(self) -> bool:
        return self.created_at + timedelta(seconds=self.TOKEN_LIFETIME_SECONDS) < timezone.now()

    @classmethod
    def create_reset_password(cls, user) -> "Token":
        return cls.objects.create(
            user=user,
            type=cls.TYPE_RESET_PASSWORD,
        )

    @classmethod
    def create_email_confirmation(cls, user) -> "Token":
        return cls.objects.create(
            user=user,
            type=cls.TYPE_EMAIL_CONFORMATION,
        )
