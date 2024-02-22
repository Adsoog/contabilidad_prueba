from django import forms
from .models import Cronograma
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CronogramaForm(forms.ModelForm):
    class Meta:
        model = Cronograma
        fields = '__all__'  # Puedes especificar los campos que desees incluir aquí

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
