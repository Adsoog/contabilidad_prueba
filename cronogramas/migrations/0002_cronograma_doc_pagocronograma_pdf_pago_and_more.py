# Generated by Django 5.0.2 on 2024-02-23 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cronogramas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cronograma',
            name='doc',
            field=models.FileField(blank=True, default=None, null=True, upload_to='pdf/'),
        ),
        migrations.AddField(
            model_name='pagocronograma',
            name='pdf_pago',
            field=models.FileField(default=None, upload_to='pagos_pdfs/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cronograma',
            name='detalle',
            field=models.CharField(max_length=255),
        ),
    ]