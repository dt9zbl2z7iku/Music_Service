from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mainapp.views import NotFoundView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('mainapp.urls')),
    path('auth/', include('authapp.urls')),
    path('not_found_404/', NotFoundView.as_view(), name='not_found')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
