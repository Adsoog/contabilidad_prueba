from django.db import models

class ExtractosBancarios(models.Model):
    TIPO_MOVIMIENTO_CHOICES = (
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    )
    banco = models.CharField(max_length=255)
    fecha_extracto = models.DateField()
    tipo_movimiento = models.CharField(max_length=7, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.banco} - {self.fecha_extracto} - {self.tipo_movimiento} - {self.cantidad}"
