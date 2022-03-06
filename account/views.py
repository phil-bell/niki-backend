from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from account.forms import ProfileForm
from account.models import Profile


class LoginView(LoginView):
    template_name = "account/login.html"


class LogoutView(LogoutView):
    template_name = "account/logout.html"


class CreateLoginView(CreateView):
    form_class = UserCreationForm
    template_name = "account/create_login.html"

    def form_valid(self, form):
        self.object = form.save()
        Profile.objects.create(user=self.object)
        authenticate(username=self.object.username, password=form.cleaned_data['password1'])
        return HttpResponseRedirect(reverse("account:profile"))


class ProfileView(TemplateView):
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_form"] = ProfileForm
        context["user_form"] = UserChangeForm
        return context
