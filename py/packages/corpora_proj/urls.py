from django.contrib import admin
from django.urls import include, path
from oauth2_provider import urls as oauth2_urls
from ninja import NinjaAPI

from corpora.api import api as corpora_router

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
