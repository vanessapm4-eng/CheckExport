from django.db import models
from apps.predios.models import Predio

class Inspeccion(models.Model):
    RESULTADO_CHOICES = [
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('condicionada', 'Condicionada'),
        ('pendiente', 'Pendiente'),
    ]
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE, related_name='inspecciones')
    funcionario_ica = models.CharField(max_length=200)
    fecha_inspeccion = models.DateField()
    resultado = models.CharField(max_length=20, choices=RESULTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Inspección'
        verbose_name_plural = 'Inspecciones'

    def __str__(self):
        return f"{self.predio} - {self.fecha_inspeccion} - {self.get_resultado_display()}"


class Certificado(models.Model):
    ESTADO_CHOICES = [
        ('vigente', 'Vigente'),
        ('vencido', 'Vencido'),
        ('cancelado', 'Cancelado'),
    ]
    inspeccion = models.OneToOneField(Inspeccion, on_delete=models.CASCADE, related_name='certificado')
    numero_certificado = models.CharField(max_length=100, unique=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='vigente')

    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'

    def __str__(self):
        return f"{self.numero_certificado} - {self.get_estado_display()}"