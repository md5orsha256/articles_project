from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView

from accounts.forms import MyUserCreationForm


class RegisterView(CreateView):
    model = User
    template_name = "registration.html"
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url

# def register_view(request):
#     form = MyUserCreationForm()
#     if request.method == "POST":
#         form = MyUserCreationForm(data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             url = request.GET.get("next")
#             if url:
#                 return redirect(url)
#             return redirect("webapp:index")
#     return render(request, "registration.html", {"form":form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('webapp:index')
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('webapp:index')
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:index')
