from django.shortcuts import render, redirect
from .models import OrdenCompra, OrdenPago
from .forms import OrdenCompraForm, OrdenPagoForm


def lista_ordenes_compra(request):
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
    context["form"] = form
    return render(request, "ordenpago.html", context)
