from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('admin-qw/', admin.site.urls),
    path('api/v1/', include('apps.api_v1')),
    path("schema-qw/", SpectacularAPIView.as_view(), name="api-schema"),
    path("docs-qw/", SpectacularSwaggerView.as_view(url_name="api-schema")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
