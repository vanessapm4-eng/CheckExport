from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.predios.urls')),
    path('checklist/', include('apps.checklist.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('reportes/', include('apps.reportes.urls')),
]