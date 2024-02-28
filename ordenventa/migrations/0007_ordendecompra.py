# Generated by Django 5.0.2 on 2024-02-28 02:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenventa', '0006_alter_ordenventa_direccion_proyecto_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenDeCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc_articulo', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField()),
                ('codigo_sap', models.CharField(max_length=50)),
                ('precio_actual', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('igv', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('detraccion', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('precio_total', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
                ('item_orden_venta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='orden_de_compra', to='ordenventa.itemordenventa')),
            ],
        ),
    ]