from django.shortcuts import get_object_or_404, render, redirect
from ordenventa.models import OrdenDeCompra, OrdenVenta
from .models import OrdenCompra, OrdenPago
from .forms import OrdenCompraForm, OrdenPagoForm
from django.http import HttpResponse
from django.template.loader import render_to_string


def lista_ordenes_compra2(request):
    ordenes_compra = OrdenCompra.objects.all()
    return render(
        request, "lista_ordenes_compra.html", {"ordenes_compra": ordenes_compra}
    )


def crear_orden_compra(request):
    if request.method == "POST":
        form = OrdenCompraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "lista_ordenes_compra"
            )  # Redirige a la lista después de guardar
    else:
        form = OrdenCompraForm()

    return render(request, "crear_orden_compra.html", {"form": form})


def ordenpago(request):
    context = {}
    form = OrdenPagoForm()
    ordenespago = OrdenPago.objects.all()
    context["ordenespago"] = ordenespago

    if request.method == "POST":
        if "save" in request.POST:
            form = OrdenPagoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("ordenpago")
        elif "delete" in request.POST:
            pk = request.POST.get("delete")
            ordenpago = OrdenPago.objects.get(id=pk)
            ordenpago.delete()
            return redirect("ordenpago")
        elif "edit" in request.POST:
            pk = request.POST.get("edit")
            ordenpago = OrdenPago.objects.get(id=pk)
            form = OrdenPagoForm(instance=ordenpago)

    context["form"] = form
    return render(request, "ordenpago.html", context)


# new methods :) ella no te quiere :P
# Vista para listar las órdenes de venta
def lista_ordenes_venta(request):

    query_codigosap = request.GET.get("codigosap", "")
    query_proyecto = request.GET.get("proyecto", "")

    ordenes_venta = OrdenVenta.objects.all().order_by("-id")

    if query_codigosap:
        ordenes_venta = ordenes_venta.filter(codigosap__icontains=query_codigosap)
    if query_proyecto:
        ordenes_venta = ordenes_venta.filter(proyecto__icontains=query_proyecto)

    if "HX-Request" in request.headers:
        # Solo devuelve el fragmento de la tabla para solicitudes HTMX
        return render(
            request,
            "fragmentos/tabla_ordenes_venta.html",
            {"ordenes_venta": ordenes_venta},
        )
    else:
        # Devuelve la página completa para solicitudes no HTMX
        return render(
            request, "lista_ordenes_venta.html", {"ordenes_venta": ordenes_venta}
        )


# Vista para mostrar las órdenes de compra de una orden de venta específica
def detalle_orden_compra(request, pk):
    orden_venta = get_object_or_404(OrdenVenta, pk=pk)
    ordenes_compra = OrdenDeCompra.objects.filter(
        item_orden_venta__ordenventa=orden_venta
    )
    return render(
        request,
        "detalle_orden_compra.html",
        {"orden_venta": orden_venta, "ordenes_compra": ordenes_compra},
    )
