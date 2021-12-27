from django.contrib.auth import views


class LoginView(views.LoginView):
    template_name = "account/login.html"


class LoginView(views.LogoutView):
    template_name = "account/logout.html"
