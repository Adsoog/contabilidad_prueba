from rest_framework import generics
from .models import OrdenVenta, ItemOrdenVenta
from .serializers import OrdenVentaSerializer, ItemOrdenVentaSerializer
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from .forms import ItemOrdenVentaForm, OrdenVentaForm, OrdenVentaUploadForm
from openpyxl import load_workbook
import openpyxl





class OrdenVentaCRUDView(View):
    template_name = "ordenventa_crud.html"

    def get(self, request, *args, **kwargs):
        # Obtén la acción de la URL (edit o delete)
        action = request.GET.get("action", None)

        # Lógica para editar
        if action == "edit":
            orden_venta_id = request.GET.get("edit", None)
            if orden_venta_id:
                orden_venta = get_object_or_404(OrdenVenta, pk=orden_venta_id)
                form = OrdenVentaForm(instance=orden_venta)
            else:
                form = OrdenVentaForm()

        # Lógica para eliminar
        elif action == "delete":
            orden_venta_id = request.GET.get("delete", None)
            if orden_venta_id:
                orden_venta = get_object_or_404(OrdenVenta, pk=orden_venta_id)
                orden_venta.delete()
                return HttpResponseRedirect(reverse_lazy("ordenventa-crud"))

        # Lógica por defecto para mostrar la lista y el formulario de creación
        else:
            form = OrdenVentaForm()

        ordenes_venta = OrdenVenta.objects.all()
        return render(
            request, self.template_name, {"ordenes_venta": ordenes_venta, "form": form}
        )

    def post(self, request, *args, **kwargs):
        form = OrdenVentaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy("ordenventa-crud"))
        else:
            ordenes_venta = OrdenVenta.objects.all()
            return render(
                request,
                self.template_name,
                {"ordenes_venta": ordenes_venta, "form": form},
            )
        
# FUNCION PARA PROCESAR EL EXCEL 
def procesar_orden_venta_excel(request, ordenventa_id):
    if request.method == "POST":
        form = OrdenVentaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_excel = request.FILES["archivo_excel"]

            # Cargar el archivo Excel con Openpyxl
            workbook = load_workbook(archivo_excel)
            sheet = workbook.active  # Si solo hay una hoja en el archivo Excel

            # Iterar sobre cada fila del archivo Excel
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Crear un objeto ItemOrdenVenta con los datos de la fila
                ItemOrdenVenta.objects.create(
                    ordenventa_id=ordenventa_id,
                    nro_articulo=row[0],
                    cantidad=row[2],
                    precio_bruto=row[6],
                    total_bruto=row[12]
                )

            return redirect("ordenventa-crud")  # Redirige a la vista correspondiente
    else:
        form = OrdenVentaUploadForm()

    return render(request, "formulario_orden_venta.html", {"form": form})

#VER LOS ITEMS SEGUN ID
def ver_items_orden_venta(request, ordenventa_id):
    ordenventa = get_object_or_404(OrdenVenta, pk=ordenventa_id)
    items = ItemOrdenVenta.objects.filter(ordenventa=ordenventa)
    
    return render(request, 'ver_items_orden_venta.html', {'ordenventa': ordenventa, 'items': items})


# REDIRIGIR LOS ITEMS
def procesar_seleccion(request, ordenventa_id):
    ordenventa = get_object_or_404(OrdenVenta, pk=ordenventa_id)

    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        action = request.POST.get('action')  # Nueva línea para obtener la acción deseada
        
        # Realizar acciones según la opción seleccionada
        if action == 'eliminar':
            # Eliminar los elementos seleccionados
            ItemOrdenVenta.objects.filter(id__in=selected_items).delete()
        elif action == 'marcar_enviado':
            # Marcar los elementos seleccionados como enviados (por ejemplo, actualizando un campo en el modelo)
            ItemOrdenVenta.objects.filter(id__in=selected_items).update(enviado=True)
        # Agrega más opciones según sea necesario

    # Redirige a la página de visualización después de procesar la selección
    return redirect('ver_items_orden_venta', ordenventa_id=ordenventa.id)


# desde aqui no hay nada interesante :P

# Vistas para OrdenVenta
class ListaOrdenesVenta(generics.ListCreateAPIView):
    queryset = OrdenVenta.objects.all()
    serializer_class = OrdenVentaSerializer


class DetalleOrdenVenta(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrdenVenta.objects.all()
    serializer_class = OrdenVentaSerializer


# Vistas para ItemOrdenVenta
class ListaItemsOrdenVenta(generics.ListCreateAPIView):
    queryset = ItemOrdenVenta.objects.all()
    serializer_class = ItemOrdenVentaSerializer


class DetalleItemOrdenVenta(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemOrdenVenta.objects.all()
    serializer_class = ItemOrdenVentaSerializer
