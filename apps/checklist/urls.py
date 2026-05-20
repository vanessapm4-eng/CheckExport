from django.urls import path
from . import views

urlpatterns = [
    path('predio/<int:predio_pk>/', views.checklist_predio, name='checklist_predio'),
    path('predio/<int:predio_pk>/item/<int:item_pk>/actualizar/', views.actualizar_item, name='actualizar_item'),
]