from django.db import models
from apps.predios.models import Predio

class Alerta(models.Model):
    TIPO_CHOICES = [
        ('vencimiento_certificado', 'Vencimiento de certificado'),
        ('vencimiento_registro', 'Vencimiento de registro ICA'),
        ('monitoreo_pendiente', 'Monitoreo pendiente'),
        ('incumplimiento', 'Incumplimiento detectado'),
    ]
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('atendida', 'Atendida'),
        ('descartada', 'Descartada'),
    ]
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE, related_name='alertas')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    fecha_alerta = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'

    def __str__(self):
        return f"{self.predio} - {self.get_tipo_display()} - {self.get_estado_display()}"