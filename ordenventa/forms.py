from django import forms
from .models import OrdenVenta, ItemOrdenVenta


class OrdenVentaForm(forms.ModelForm):
    class Meta:
        model = OrdenVenta
        fields = ["codigosap", "proyecto", "direccion_proyecto", "observacion", "fecha"]


class ItemOrdenVentaForm(forms.ModelForm):
    class Meta:
        model = ItemOrdenVenta
        fields = ["nro_articulo", "cantidad", "precio_bruto", "total_bruto"]

class OfertaVentaUploadForm(forms.Form):
    archivo_excel = forms.FileField(label='Selecciona un archivo Excel')

class OrdenVentaUploadForm(forms.Form):
    archivo_excel = forms.FileField(label='Selecciona un archivo Excel')

