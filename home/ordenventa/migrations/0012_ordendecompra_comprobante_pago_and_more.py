# Generated by Django 5.0.2 on 2024-03-03 14:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenventa', '0011_ordendecompra_cuotas'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordendecompra',
            name='comprobante_pago',
            field=models.FileField(blank=True, null=True, upload_to='comprobantes_pago/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Comprobante de Pago'),
        ),
        migrations.AddField(
            model_name='ordendecompra',
            name='fecha_pago',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Pago'),
        ),
    ]
