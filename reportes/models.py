from django.db import models

# Create your models here.

class Proveedor(models.Model):
    ruc_dni = models.CharField(max_length=20, unique=True, verbose_name="RUC/DNI")
    nombre_proveedor = models.CharField(max_length=100, verbose_name="Nombre del Proveedor")
    nombre_banco = models.CharField(max_length=100, verbose_name="Nombre del Banco")
    moneda = models.CharField(max_length=10, choices=(('USD', 'Dólar Americano'), ('PEN', 'Sol Peruano')), default='PEN', verbose_name="Moneda")
    nro_cuenta = models.CharField(max_length=50, verbose_name="Número de Cuenta")

    def __str__(self):
        return f"{self.nombre_proveedor} - {self.ruc_dni}"

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"