import os
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static('/media', document_root=settings.MEDIA_ROOT)
    urlpatterns += static('/entities', document_root=settings.ENTITIES_ROOT)
