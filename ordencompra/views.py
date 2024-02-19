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

    if request.method == 'POST':
        if 'save' in request.POST:
            form = OrdenPagoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('ordenpago')
        elif 'delete' in request.POST:
            pk = request.POST.get('delete') 
            ordenpago = OrdenPago.objects.get(id=pk)
            ordenpago.delete()
            return redirect('ordenpago')
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            ordenpago = OrdenPago.objects.get(id=pk)
            form = OrdenPagoForm(instance=ordenpago)
    
    context["form"] = form
    return render(request, "ordenpago.html", context)

