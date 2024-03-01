from django import forms
from .models import Cronograma, PagoCronograma
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CronogramaForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_desembolso = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    # Agrega cualquier otro campo de fecha que necesites de manera similar

    class Meta:
        model = Cronograma
        fields = "__all__"  # O especifica los campos que necesitas

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Guardar"))

        # Aplica estilos a otros campos si es necesario
        for field_name, field in self.fields.items():
            if field_name not in ['fecha_inicio', 'fecha_fin']:  # Evita sobrescribir la clase para los campos de fecha ya definidos
                field.widget.attrs["class"] = "form-control"

# forms htmx
class EditarMontoForm(forms.ModelForm):
    class Meta:
        model = PagoCronograma
        fields = ["monto_pago"]
        widgets = {
            "monto_pago": forms.NumberInput(attrs={"step": "0.01"}),
        }


class CambiarPDFPagoForm(forms.ModelForm):
    class Meta:
        model = PagoCronograma
        fields = ["pdf_pago"]


class EditarFechaPagoForm(forms.ModelForm):
    class Meta:
        model = PagoCronograma
        fields = ["fecha_pago"]
        widgets = {
            "fecha_pago": forms.DateInput(attrs={"type": "date"}),
        }
