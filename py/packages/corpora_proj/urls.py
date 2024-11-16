from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from oauth2_provider import urls as oauth2_urls
from ninja import NinjaAPI

from corpora.router import api as corpora_router
from corpora.views import BinaryView

router = NinjaAPI(
    title="Corpora API",
    version="0.1.0",
    description="API for managing and processing corpora",
)
router.add_router("corpora", corpora_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("o/", include(oauth2_urls)),
    path("api/", router.urls),
    path("api/docs", router.get_openapi_schema),
]

if settings.DEBUG:
    urlpatterns += [
        path("bin/<str:arch>/", BinaryView.as_view(), name="binary"),
    ]
