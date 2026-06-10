from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('predios/nuevo/', views.crear_predio, name='crear_predio'),
    path('predios/<int:predio_pk>/editar/', views.editar_predio, name='editar_predio'),
    path('predios/<int:predio_pk>/eliminar/', views.eliminar_predio, name='eliminar_predio'),
]