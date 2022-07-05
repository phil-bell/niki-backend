from account.forms import ProfileForm
from account.models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView


class LoginView(LoginView):
    template_name = "account/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("account:profile"))
        return super().get(request, *args, **kwargs)


class LogoutView(LogoutView):
    template_name = "account/logout.html"


class CreateLoginView(CreateView):
    form_class = UserCreationForm
    template_name = "account/create_login.html"

    def form_valid(self, form):
        self.object = form.save()
        Profile.objects.create(user=self.object)
        user = authenticate(
            reuqest=self.request,
            username=self.object.username,
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return HttpResponseRedirect(reverse("account:profile"))


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = "account:login"
    template_name = "account/profile.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print(f"user: {request.user}")
        profile = Profile.objects.get(user=request.user)
        context["profile_form"] = ProfileForm(instance=profile)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse()
        return HttpResponse(status=400)
