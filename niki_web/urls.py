from django.contrib import admin
from django.urls import include, path

from account.views import LoginView

urlpatterns = [
    path("", LoginView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path("account/", include("account.urls")),
    path("search/", include("search.urls")),
]
