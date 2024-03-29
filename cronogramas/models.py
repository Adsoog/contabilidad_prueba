from django.db import models

# Create your models here.from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class Cronograma(models.Model):
    fecha_inicio = models.DateField()
    fecha_desembolso = models.DateField()
    entidad = models.CharField(max_length=100)
    moneda = models.CharField(max_length=50)
    numero_cuotas = models.PositiveIntegerField()
    monto_cuota = models.DecimalField(max_digits=15, decimal_places=2)
    monto_total = models.DecimalField(max_digits=15, decimal_places=2)
    detalle = models.CharField(
        max_length=255
    )  # Ajusta la longitud máxima según sea necesario
    doc = models.FileField(upload_to="pdf/", null=True, blank=True, default=None)

    def __str__(self):
        return f"Cronograma {self.id} - {self.entidad} - {self.detalle}"


class PagoCronograma(models.Model):
    cronograma = models.ForeignKey(Cronograma, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    monto_pago = models.DecimalField(max_digits=15, decimal_places=2)
    pdf_pago = models.FileField(
        upload_to="pagos_pdfs/", null=True, blank=True, default=None
    )  # Campo para guardar archivos PDF de pagos

    def __str__(self):
        return f"Pago de {self.monto_pago} el {self.fecha_pago} - Detalle: {self.cronograma.detalle}"


@receiver(post_save, sender=Cronograma)
def crear_pagos(sender, instance, created, **kwargs):
    if created:
        fecha_actual = instance.fecha_inicio
        for i in range(instance.numero_cuotas):
            # Ajuste especial para el cuarto pago
            if i == 3:
                fecha_actual += relativedelta(months=2)
            # Ajuste especial para el sexto pago
            elif i == 5:
                fecha_actual += relativedelta(months=5)
            else:
                fecha_actual += relativedelta(months=1)

            PagoCronograma.objects.create(
                cronograma=instance,
                fecha_pago=fecha_actual,
                monto_pago=instance.monto_cuota,
            )
class Resolucion(models.Model):
    numero_resolucion = models.CharField(max_length=255)
    tipo_resolucion = models.CharField(max_length=255)
    tiempo_aplazamiento = models.CharField(max_length=255)
    archivo_pdf = models.FileField(upload_to='pdfs/')
    descripcion = models.TextField()  # Campo añadido para la descripción
    monto_tributo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    interes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.numero_resolucion

#este otro no
class DetallePago(models.Model):
    resolucion = models.ForeignKey(
        Resolucion, on_delete=models.CASCADE, related_name="detalles_pago"
    )
    id_pago = models.CharField(max_length=10)
    vencimiento = models.DateField()
    amortizacion = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)


#este sirve
class Pago(models.Model):
    resolucion = models.ForeignKey(Resolucion, related_name='pagos', on_delete=models.CASCADE)
    numero_cuota = models.CharField(max_length=255)
    vencimiento = models.DateField()
    amortizacion = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    pago_sunat = models.FileField(upload_to='pagos_sunat/', null=True, blank=True)  # Campo opcional para archivo PDF

    def __str__(self):
        return f"{self.resolucion} - Cuota {self.numero_cuota}"