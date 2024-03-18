# Generated by Django 5.0.2 on 2024-03-12 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenventa', '0016_cobrosordenventa'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacturaElectronica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie_correlativo', models.CharField(max_length=100, verbose_name='Serie y Correlativo')),
                ('fecha_emision', models.DateField(verbose_name='Fecha de Emisión')),
                ('cliente', models.CharField(max_length=255, verbose_name='Cliente')),
                ('ruc_cliente', models.CharField(max_length=11, verbose_name='RUC Cliente')),
                ('tipo_moneda', models.CharField(max_length=20, verbose_name='Tipo de Moneda')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('importe_total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Importe Total')),
                ('detraccion', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Detracción')),
                ('monto_neto_cobrar', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto Neto a Cobrar')),
                ('total_cuotas', models.IntegerField(verbose_name='Total de Cuotas')),
                ('fecha_vencimiento', models.DateField(verbose_name='Fecha de Vencimiento')),
            ],
        ),
    ]