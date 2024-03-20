# Generated by Django 5.0.2 on 2024-03-19 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extractos', '0002_banco_remove_extractosbancarios_cantidad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extractosbancarios',
            name='banco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='extractos.banco', verbose_name='Banco'),
        ),
        migrations.AlterField(
            model_name='extractosbancarios',
            name='fecha_operacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Operación'),
        ),
        migrations.AlterField(
            model_name='extractosbancarios',
            name='importe',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='extractosbancarios',
            name='itf',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='ITF'),
        ),
        migrations.AlterField(
            model_name='extractosbancarios',
            name='numero_movimiento',
            field=models.CharField(default='', max_length=50, verbose_name='Número de Movimiento'),
        ),
        migrations.AlterField(
            model_name='extractosbancarios',
            name='referencia',
            field=models.CharField(default='', max_length=100),
        ),
    ]
