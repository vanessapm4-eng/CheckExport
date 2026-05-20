from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('productor', 'Productor exportador'),
        ('inspector', 'Inspector ICA'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='productor')
    telefono = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"