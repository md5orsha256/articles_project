from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, UserProfileView, UpdateUserView, UserPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path("<int:pk>/", UserProfileView.as_view(), name="user-profile"),
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('registration/', RegisterView.as_view(), name="registration"),
    path("update/", UpdateUserView.as_view(), name="update-user"),
    path("change-password/", UserPasswordChangeView.as_view(), name="change-password")
]
