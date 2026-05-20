from django.contrib import admin
from .models import Predio, UsuarioPredio

@admin.register(Predio)
class PredioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'registro_ica', 'municipio', 'estado_habilitacion']
    list_filter = ['estado_habilitacion', 'departamento']
    search_fields = ['nombre', 'registro_ica']

@admin.register(UsuarioPredio)
class UsuarioPredioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'predio', 'rol']