
from django.urls.conf import path

from .views import LoginView, LogoutView

app_name = "account"

urlpatterns = [
    path(r"^login/$", LoginView.as_view(), name="login"),
    path(r"^logout/$", LogoutView.as_view(), name="logout"),
]

