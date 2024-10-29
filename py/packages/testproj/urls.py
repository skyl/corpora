"""
URL configuration for testproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

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
