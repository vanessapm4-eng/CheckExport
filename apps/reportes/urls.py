from django.urls import path
from . import views

urlpatterns = [
    path('pdf/<int:predio_pk>/', views.reporte_pdf, name='reporte_pdf'),
]