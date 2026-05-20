from django.db import models
from django.conf import settings
from apps.predios.models import Predio

class MonitoreoPlaga(models.Model):
    NIVEL_CHOICES = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
        ('critico', 'Crítico'),
    ]
    PLAGA_CHOICES = [
        ('trips', 'Trips'),
        ('acaros', 'Ácaros'),
        ('mosca_blanca', 'Mosca blanca'),
        ('otro', 'Otro'),
    ]
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE, related_name='monitoreos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    tipo_plaga = models.CharField(max_length=50, choices=PLAGA_CHOICES)
    nivel_infestacion = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    fecha_monitoreo = models.DateField()
    observaciones = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Monitoreo de plaga'
        verbose_name_plural = 'Monitoreos de plagas'

    def __str__(self):
        return f"{self.predio} - {self.tipo_plaga} - {self.fecha_monitoreo}"


class AplicacionFitosanitaria(models.Model):
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE, related_name='aplicaciones')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    producto = models.CharField(max_length=200)
    dosis = models.CharField(max_length=100)
    lote = models.CharField(max_length=100, blank=True)
    fecha_aplicacion = models.DateField()
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Aplicación fitosanitaria'
        verbose_name_plural = 'Aplicaciones fitosanitarias'

    def __str__(self):
        return f"{self.predio} - {self.producto} - {self.fecha_aplicacion}"