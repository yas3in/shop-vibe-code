from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include("accounts.urls.web")),
    path("accounts/panel/", include("accounts.urls.panel")),

    path("addresses/", include("addresses.urls.web")),
    path("addresses/panel/", include("addresses.urls.panel")),

    path("catalog/", include("catalog.urls.web")),
    path("panel/catalog/", include("catalog.urls.panel")),

    path("orders/", include("orders.urls.web")),
    path("orders/panel/", include("orders.urls.panel")),

    path("payments/", include("orders.urls.payment")),

    path("", include("core.urls.web")),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )
