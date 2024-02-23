from django.db import models

# Create your models here.
class OrdenVenta(models.Model):
    codigosap = models.CharField(max_length=50)
    proyecto = models.CharField(max_length=255)
    direccion_proyecto = models.CharField(max_length=255)
    observacion = models.CharField(max_length=255)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.codigosap} - {self.proyecto} - {self.direccion_proyecto}"
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
        return f"{self.nro_articulo} - {self.ordenventa}"