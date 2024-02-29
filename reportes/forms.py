from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['ruc_dni', 'nombre_proveedor', 'nombre_banco', 'moneda', 'nro_cuenta']
        widgets = {
            'ruc_dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_banco': forms.TextInput(attrs={'class': 'form-control'}),
            'moneda': forms.Select(attrs={'class': 'form-control'}),
            'nro_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
        }
