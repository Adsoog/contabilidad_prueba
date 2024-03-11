# Generated by Django 5.0.2 on 2024-03-11 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExtractosBancarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banco', models.CharField(max_length=255)),
                ('fecha_extracto', models.DateField()),
                ('tipo_movimiento', models.CharField(choices=[('ingreso', 'Ingreso'), ('egreso', 'Egreso')], max_length=7)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
