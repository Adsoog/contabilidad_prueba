# Generated by Django 5.0.2 on 2024-03-11 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenventa', '0012_ordendecompra_comprobante_pago_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordendecompra',
            name='monto_detraccion',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
    ]