# Generated by Django 5.0.2 on 2024-02-29 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenventa', '0010_ordendecompra_clase_alter_ordendecompra_proveedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordendecompra',
            name='cuotas',
            field=models.IntegerField(default=0),
        ),
    ]
