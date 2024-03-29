# Generated by Django 5.0.2 on 2024-02-14 02:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigosap', models.CharField(max_length=50)),
                ('proyecto', models.CharField(max_length=255)),
                ('direccion_proyecto', models.TextField()),
                ('observacion', models.TextField()),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ItemOrdenVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro_articulo', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField()),
                ('precio_bruto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_bruto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ordenventa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ordenventa.ordenventa')),
            ],
        ),
    ]
