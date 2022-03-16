from accounts.views.register import RegisterView, EmailConfirmView
from accounts.views.profile import UserProfileView, UpdateUserView
from accounts.views.password import (
    UserPasswordChangeView,
    ForgotPasswordView,
    ResetPasswordView,
)


__all__ = (
    "RegisterView",
    "EmailConfirmView",
    "UserProfileView",
    "UpdateUserView",
    "UserPasswordChangeView",
    "ForgotPasswordView",
    "ResetPasswordView",
)
