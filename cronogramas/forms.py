from django import forms
from .models import Cronograma, PagoCronograma
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CronogramaForm(forms.ModelForm):
    class Meta:
        model = Cronograma
        fields = "__all__"  # Puedes especificar los campos que desees incluir aquí

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Guardar"))

        for field_name, field in self.fields.items():
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
