from django.db import models

# Create your models here.from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class Cronograma(models.Model):
    fecha_inicio = models.DateField()
    fecha_desembolso = models.DateField()
    entidad_bancaria = models.CharField(max_length=100)
    moneda = models.CharField(max_length=50)
    numero_cuotas = models.PositiveIntegerField()
    monto_cuota = models.DecimalField(max_digits=15, decimal_places=2)
    monto_total = models.DecimalField(max_digits=15, decimal_places=2)
    detalle = models.CharField(max_length=255)  # Ajusta la longitud máxima según sea necesario
    doc = models.FileField(upload_to='pdf/', null=True, blank=True, default=None)

    def __str__(self):
        return f"Cronograma {self.id} - {self.entidad_bancaria} - {self.detalle}"

class PagoCronograma(models.Model):
    cronograma = models.ForeignKey(Cronograma, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    monto_pago = models.DecimalField(max_digits=15, decimal_places=2)
    pdf_pago = models.FileField(upload_to='pagos_pdfs/')  # Campo para guardar archivos PDF de pagos

    def __str__(self):
        return f"Pago de {self.monto_pago} el {self.fecha_pago}"

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
                monto_pago=instance.monto_cuota
            )