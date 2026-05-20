from django.db import models
from django.conf import settings
from apps.predios.models import Predio

class FaseChecklist(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Fase del checklist'

    def __str__(self):
        return f"{self.orden}. {self.nombre}"


class ItemChecklist(models.Model):
    fase = models.ForeignKey(FaseChecklist, on_delete=models.CASCADE, related_name='items')
    descripcion = models.TextField(verbose_name='Requisito fitosanitario')
    es_obligatorio = models.BooleanField(default=True)
    norma_referencia = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.descripcion[:70]


class RegistroChecklist(models.Model):
    ESTADO_CHOICES = [
        ('cumple', 'Cumple'),
        ('no_cumple', 'No cumple'),
        ('na', 'No aplica'),
        ('pendiente', 'Pendiente'),
    ]
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE, related_name='registros_checklist')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(ItemChecklist, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observacion = models.TextField(blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('predio', 'item')
        verbose_name = 'Registro de checklist'