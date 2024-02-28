from rest_framework import generics
from django.http import HttpResponse, JsonResponse
from inventario.models import Inventario
from .models import OrdenDeCompra, OrdenVenta, ItemOrdenVenta
from .serializers import OrdenVentaSerializer, ItemOrdenVentaSerializer
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from .forms import ItemOrdenVentaForm, OrdenVentaForm, OrdenVentaUploadForm
from openpyxl import load_workbook
from django.db import transaction
from django.template.loader import render_to_string


# antiguos view debemos depurar despues
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


def procesar_seleccion(request, ordenventa_id):
    if request.method == "POST":
        selected_items = request.POST.getlist("selected_items")
        action = request.POST.get("action")

        if action == "eliminar":
            # Elimina los ítems seleccionados
            ItemOrdenVenta.objects.filter(id__in=selected_items).delete()
        elif action == "marcar_enviado":
            # Marca como enviado los ítems seleccionados
            ItemOrdenVenta.objects.filter(id__in=selected_items).update(enviado=True)

        # Redirige según la acción
        return redirect("ver_items_orden_venta", ordenventa_id=ordenventa_id)

    return redirect("ordenventa_crud")


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
                    desc_articulo=row[1],
                    cantidad=row[2],
                    precio_bruto=row[6],
                    total_bruto=row[12],
                )

            return redirect(
                "ver_items_orden_venta", ordenventa_id=ordenventa_id
            )  # Redirige a la vista correspondiente
    else:
        form = OrdenVentaUploadForm()

    return render(request, "formulario_orden_venta.html", {"form": form})


# VER LOS ITEMS SEGUN ID
def ver_items_orden_venta(request, ordenventa_id):
    ordenventa = get_object_or_404(OrdenVenta, pk=ordenventa_id)
    items = ItemOrdenVenta.objects.filter(ordenventa=ordenventa)

    # Verificar si la solicitud es una solicitud HTMX
    if request.headers.get("HX-Request", "false").lower() == "true":
        html = render_to_string("fragmentos/items_orden_venta.html", {"items": items})
        return JsonResponse({"html": html})

    return render(
        request,
        "ver_items_orden_venta.html",
        {"ordenventa": ordenventa, "items": items},
    )


def ver_items_orden_venta2(request, ordenventa_id):
    ordenventa = get_object_or_404(OrdenVenta, pk=ordenventa_id)
    items = ItemOrdenVenta.objects.filter(ordenventa=ordenventa)

    # Obtener los nro_articulo de los items de la orden de venta
    nros_articulos = [item.nro_articulo for item in items]

    # Filtrar los registros de Inventario que coinciden con los nro_articulo de los items
    inventario = Inventario.objects.filter(num_articulo__in=nros_articulos)

    return render(
        request,
        "ver_items_orden_venta2.html",
        {"ordenventa": ordenventa, "items": items, "inventario": inventario},
    )


# VER LOS ITEMS SEGUN ENVIADOS Y LUEGO PROCESAR CON DEMS FUNCIONES
def ver_items_enviados_orden_venta(request, ordenventa_id):
    ordenventa = get_object_or_404(OrdenVenta, pk=ordenventa_id)
    items_enviados = ItemOrdenVenta.objects.filter(ordenventa=ordenventa, enviado=True)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = []
        for item in items_enviados:
            data.append(
                {
                    "desc_articulo": item.desc_articulo,
                    "cantidad": item.cantidad,
                    "precio_bruto": item.precio_bruto,
                    "total_bruto": item.total_bruto,
                }
            )
        return JsonResponse(data, safe=False)

    return render(
        request,
        "ver_items_enviados_orden_venta.html",
        {"ordenventa": ordenventa, "items_enviados": items_enviados},
    )


# ORDEN AUTOMATICAS
def ver_ordenes_compra(request, ordenventa_id):
    ordenventa = get_object_or_404(OrdenVenta, pk=ordenventa_id)
    ordenes_compra = OrdenDeCompra.objects.filter(
        item_orden_venta__ordenventa=ordenventa
    )
    return render(
        request,
        "ver_orden_compra.html",
        {"ordenes_compra": ordenes_compra, "ordenventa": ordenventa},
    )


# mas ordenes automaticas :P
def actualizar_orden_de_compra(request, id):
    if request.method == "POST":
        orden_de_compra = get_object_or_404(OrdenDeCompra, pk=id)

        # Asegúrate de actualizar los campos de orden_de_compra con los datos recibidos
        orden_de_compra.cantidad = request.POST.get(
            "cantidad", orden_de_compra.cantidad
        )
        orden_de_compra.precio_actual = request.POST.get(
            "precio_actual", orden_de_compra.precio_actual
        )
        orden_de_compra.igv = request.POST.get("igv", orden_de_compra.igv)
        orden_de_compra.detraccion = request.POST.get(
            "detraccion", orden_de_compra.detraccion
        )

        orden_de_compra.save()

        # En lugar de redirigir, devuelve un fragmento de HTML o texto para actualizar la página
        return HttpResponse(f"{orden_de_compra.precio_total}")


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
