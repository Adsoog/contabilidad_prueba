from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Definición de los modelos
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
    item_orden_venta = models.OneToOneField(
        ItemOrdenVenta, on_delete=models.CASCADE, related_name="orden_de_compra"
    )
    clase = models.CharField(
        max_length=50, default=""
    )  # Campo opcional con valor predeterminado vacío
    desc_articulo = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    codigo_sap = models.CharField(max_length=50)
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    igv = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Porcentaje
    detraccion = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )  # Porcentaje
    precio_total = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0
    )
    proveedor = models.CharField(
        max_length=100, default=""
    )  # Campo opcional con valor predeterminado vacío
    banco = models.CharField(
        max_length=100, default=""
    )  # Campo opcional con valor predeterminado vacío
    numero_bancario = models.CharField(
        max_length=50, default=""
    )  # Campo opcional con valor predeterminado vacío
    cuotas = models.IntegerField(
        default=0, blank=True, null=True
    )  # Campo opcional que puede ser nulo

    def save(self, *args, **kwargs):
        self.precio_total = self.cantidad * self.precio_actual * (
            1 + self.igv / 100
        ) - (self.cantidad * self.precio_actual * self.detraccion / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.desc_articulo} - {self.cantidad} - {self.codigo_sap}"


# Señal para crear o actualizar OrdenDeCompra cuando se guarda un ItemOrdenVenta
@receiver(post_save, sender=ItemOrdenVenta)
def create_or_update_orden_de_compra(sender, instance, created, **kwargs):
    OrdenDeCompra.objects.update_or_create(
        item_orden_venta=instance,
        defaults={
            "desc_articulo": instance.desc_articulo,
            "cantidad": instance.cantidad,
            "codigo_sap": instance.ordenventa.codigosap,
            "precio_actual": 0,  # Asumiendo un valor por defecto
            "igv": 0,  # Valor por defecto, actualizable posteriormente
            "detraccion": 0,  # Valor por defecto, actualizable posteriormente
            # No es necesario definir precio_total aquí ya que se calcula en el método save de OrdenDeCompra
        },
    )
