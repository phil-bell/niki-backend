
from django.urls.conf import path

from account.views import LoginView, LogoutView, CreateLoginView, ProfileView

app_name = "account"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("create/", CreateLoginView.as_view(), name="create"),
    path("profile/", ProfileView.as_view(), name="profile"),
]

