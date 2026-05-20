from django.db import models
from django.conf import settings

class Predio(models.Model):
    ESTADO_CHOICES = [
        ('habilitado', 'Habilitado'),
        ('suspendido', 'Suspendido'),
        ('en_proceso', 'En proceso de habilitación'),
    ]
    nombre = models.CharField(max_length=200)
    registro_ica = models.CharField(max_length=100, unique=True)
    municipio = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    vereda = models.CharField(max_length=100, blank=True)
    hectareas = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    estado_habilitacion = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='en_proceso')
    fecha_vencimiento_registro = models.DateField(null=True, blank=True)
    usuarios = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UsuarioPredio',
        related_name='predios'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def porcentaje_cumplimiento(self):
        registros = self.registros_checklist.exclude(estado='na')
        if not registros.exists():
            return 0
        cumple = registros.filter(estado='cumple').count()
        return round((cumple / registros.count()) * 100)

    def nivel_riesgo(self):
        pct = self.porcentaje_cumplimiento()
        if pct >= 80: return 'bajo'
        if pct >= 50: return 'medio'
        return 'alto'

    def alertas_activas(self):
        return self.alertas.filter(estado='activa').count()

    def __str__(self):
        return f"{self.nombre} ({self.registro_ica})"

    class Meta:
        verbose_name = 'Predio'
        verbose_name_plural = 'Predios'


class UsuarioPredio(models.Model):
    ROL_CHOICES = [('admin', 'Administrador'), ('operador', 'Operador')]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='operador')
    fecha_asignacion = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'predio')