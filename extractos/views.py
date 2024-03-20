from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_htmx.http import trigger_client_event
from .models import Banco, ExtractosBancarios
from .forms import BancoForm, CargaExtractoForm  # Asumiendo que tienes un formulario definido en forms.py
import pandas as pd
from django.views.generic.edit import FormView

class BancoListView(ListView):
    model = Banco
    context_object_name = 'bancos'
    template_name = 'bancos/banco_list.html'

class BancoCreateView(CreateView):
    model = Banco
    form_class = BancoForm
    template_name = 'bancos/banco_form.html'
    success_url = reverse_lazy('banco_list')

class BancoUpdateView(UpdateView):
    model = Banco
    form_class = BancoForm
    template_name = 'bancos/banco_form.html'
    success_url = reverse_lazy('banco_list')

class BancoDeleteView(DeleteView):
    model = Banco
    context_object_name = 'banco'
    template_name = 'bancos/banco_confirm_delete.html'
    success_url = reverse_lazy('banco_list')


class BancoCreateExtracto(FormView):
    template_name = 'extractos/cargar_extractos_banco.html'
    form_class = CargaExtractoForm
    success_url = reverse_lazy('banco_list')  # Ajusta esto según tus necesidades

    def form_valid(self, form):
        # Obtiene el banco seleccionado del formulario
        banco = form.cleaned_data['banco']
        archivo_excel = self.request.FILES['archivo_excel']
        
        # Procesamiento del archivo Excel
        nombre_hoja = str(banco.nombre_banco)
        df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja, header=2)
        
        mapeo_nombres = {
            'F.Operac.': 'fecha_operacion',
            'Referencia': 'referencia',
            'Importe': 'importe',
            'ITF': 'itf',
            'Num.Mvto': 'numero_movimiento',
        }

        df.rename(columns=mapeo_nombres, inplace=True)
        df = df[list(mapeo_nombres.values())]
        df.dropna(subset=['fecha_operacion', 'numero_movimiento'], inplace=True)
        df['fecha_operacion'] = pd.to_datetime(df['fecha_operacion'], errors='coerce')
        df['importe'] = pd.to_numeric(df['importe'], errors='coerce')
        df['itf'] = pd.to_numeric(df['itf'], errors='coerce')
        df['numero_movimiento'] = df['numero_movimiento'].astype(int)
        
        for _, row in df.iterrows():
            ExtractosBancarios.objects.create(
                banco=banco,
                fecha_operacion=row['fecha_operacion'],
                referencia=row['referencia'],
                importe=row['importe'],
                itf=row['itf'],
                numero_movimiento=row['numero_movimiento'],
            )

        return super().form_valid(form)



# extractos view vamos...
def carga_extracto(request):
    if request.method == 'POST':
        form = CargaExtractoForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtiene el banco seleccionado del formulario
            banco = form.cleaned_data['banco']
            archivo_excel = request.FILES['archivo_excel']
            
            # Procesamiento del archivo Excel
            nombre_hoja = str(banco.nombre_banco)
            df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja, header=2)
            
            mapeo_nombres = {
                'F.Operac.': 'fecha_operacion',
                'Referencia': 'referencia',
                'Importe': 'importe',
                'ITF': 'itf',
                'Num.Mvto': 'numero_movimiento',
            }

            df.rename(columns=mapeo_nombres, inplace=True)
            df = df[list(mapeo_nombres.values())]
            df.dropna(subset=['fecha_operacion', 'numero_movimiento'], inplace=True)
            df['fecha_operacion'] = pd.to_datetime(df['fecha_operacion'], errors='coerce')
            df['importe'] = pd.to_numeric(df['importe'], errors='coerce')
            df['itf'] = pd.to_numeric(df['itf'], errors='coerce')
            df['numero_movimiento'] = df['numero_movimiento'].astype(int)
            
            for _, row in df.iterrows():
                ExtractosBancarios.objects.create(
                    banco=banco,
                    fecha_operacion=row['fecha_operacion'],
                    referencia=row['referencia'],
                    importe=row['importe'],
                    itf=row['itf'],
                    numero_movimiento=row['numero_movimiento'],
                )
            
            return redirect('cargar_extractos')
    else:
        form = CargaExtractoForm()

    return render(request, 'extractos/cargar_extractos.html', {'form': form})

# listar extratos
def extractos_por_banco(request, banco_id):
    banco = get_object_or_404(Banco, pk=banco_id)
    extractos = ExtractosBancarios.objects.filter(banco=banco)
    return render(request, 'extractos/extractos_por_banco.html', {'banco': banco, 'extractos': extractos})
