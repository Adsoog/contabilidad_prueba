from django.db import models


# Create your models here.
class OrdenVenta(models.Model):
    codigosap = models.CharField(max_length=50)
    proyecto = models.CharField(max_length=255)
    direccion_proyecto = models.CharField(max_length=255)
    observacion = models.CharField(max_length=255)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.codigosap} - {self.proyecto} - {self.observacion}"


class ItemOrdenVenta(models.Model):
    ordenventa = models.ForeignKey(
        OrdenVenta, related_name="items", on_delete=models.CASCADE
    )
    nro_articulo = models.CharField(max_length=50, null=True, default="")
    desc_articulo = models.CharField(max_length=50, null=True, default="")
    cantidad = models.IntegerField(null=True, default=0)
    precio_bruto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_bruto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    enviado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nro_articulo} - {self.ordenventa} - {self.desc_articulo}"


class OrdenDeCompra(models.Model):
    desc_articulo = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    codigo_sap = models.CharField(
        max_length=50
    )  # Suponiendo que este es el campo adicional
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    igv = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )  # Porcentaje, ej. 18 para 18%
    detraccion = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )  # Porcentaje
    precio_total = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0
    )

    def save(self, *args, **kwargs):
        # Calculamos el precio total aquí
        base = self.cantidad * self.precio_actual
        igv_total = base * (self.igv / 100)
        detraccion_total = base * (self.detraccion / 100)
        self.precio_total = base + igv_total - detraccion_total

        super().save(*args, **kwargs)  # No olvides llamar al método save del padre!

    def __str__(self):
        return f"{self.desc_articulo} - {self.cantidad} - {self.codigo_sap}"
