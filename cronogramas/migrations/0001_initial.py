# Generated by Django 5.0.2 on 2024-02-22 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cronograma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_desembolso', models.DateField()),
                ('entidad_bancaria', models.CharField(max_length=100)),
                ('moneda', models.CharField(max_length=50)),
                ('numero_cuotas', models.PositiveIntegerField()),
                ('monto_cuota', models.DecimalField(decimal_places=2, max_digits=15)),
                ('monto_total', models.DecimalField(decimal_places=2, max_digits=15)),
                ('detalle', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PagoCronograma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateField()),
                ('monto_pago', models.DecimalField(decimal_places=2, max_digits=15)),
                ('cronograma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cronogramas.cronograma')),
            ],
        ),
    ]
