# Generated by Django 5.0.2 on 2024-03-05 01:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cronogramas', '0008_resolucion_descripcion_resolucion_interes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='pago_sunat',
            field=models.FileField(blank=True, null=True, upload_to='pagos_sunat/'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='resolucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos', to='cronogramas.resolucion'),
        ),
    ]
