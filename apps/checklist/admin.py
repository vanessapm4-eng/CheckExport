from django.contrib import admin
from .models import FaseChecklist, ItemChecklist, RegistroChecklist

@admin.register(FaseChecklist)
class FaseAdmin(admin.ModelAdmin):
    list_display = ['orden', 'nombre']

@admin.register(ItemChecklist)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['fase', 'descripcion', 'es_obligatorio']
    list_filter = ['fase']

@admin.register(RegistroChecklist)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ['predio', 'item', 'estado', 'fecha_registro']
    list_filter = ['estado']