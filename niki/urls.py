from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api.views import (
    KeyViewset,
    LocationViewset,
    SearchView,
    ServerViewset,
    TorrentViewset,
)

router = routers.DefaultRouter()
# router.register(r"user", UserViewSet)
router.register(r"server", ServerViewset)
router.register(r"location", LocationViewset)
router.register(r"torrent", TorrentViewset)
router.register(r"key", KeyViewset, basename="key")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/search/", SearchView.as_view(), name="search"),
    path("api/", include(router.urls)),
]
