from django import forms
from .models import OrdenVenta, ItemOrdenVenta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class OrdenVentaForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )   
    class Meta:
        model = OrdenVenta
        fields = ["codigosap", "proyecto", "direccion_proyecto", "observacion", "fecha"]

    def __init__(self, *args, **kwargs):
        super(OrdenVentaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
        'codigosap',
            'proyecto',
            'direccion_proyecto',
            'observacion',
            'fecha',
            Submit('submit', 'Guardar', css_class='btn btn-primary mt-2')
        )


class ItemOrdenVentaForm(forms.ModelForm):
    class Meta:
        model = ItemOrdenVenta
        fields = ['nro_articulo', 'desc_articulo', 'cantidad', 'precio_bruto', 'total_bruto']

class OfertaVentaUploadForm(forms.Form):
    archivo_excel = forms.FileField(label='Selecciona un archivo Excel')

class OrdenVentaUploadForm(forms.Form):
    archivo_excel = forms.FileField(label='Selecciona un archivo Excel')

