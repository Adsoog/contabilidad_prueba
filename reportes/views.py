from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from ordenventa.models import OrdenVenta, ItemOrdenVenta
from reportes.forms import ProveedorForm
from reportes.models import Proveedor
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


def reportes_registros(request):
    return render(request, 'reportes_registros.html')   

    

##### PROVEEDORES CUIDADO :T
class ProveedorListView(ListView):
    model = Proveedor
    context_object_name = 'proveedores'
    template_name = 'proveedores/proveedor_list.html'

class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedor_list')
    template_name = 'proveedores/proveedor_form.html'

class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedor_list')
    template_name = 'proveedores/proveedor_form.html'

class ProveedorDeleteView(DeleteView):
    model = Proveedor
    success_url = reverse_lazy('proveedor_list')
    template_name = 'proveedores/proveedor_confirm_delete.html'