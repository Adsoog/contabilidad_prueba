import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .forms import EditarFechaPagoForm, EditarMontoForm, CambiarPDFPagoForm
from .models import PagoCronograma
from cronogramas.models import Cronograma, PagoCronograma
from .forms import CronogramaForm  # Importa el formulario de Cronograma


def crear_cronograma(request):
    if request.method == "POST":
        form = CronogramaForm(request.POST)
        if form.is_valid():
            cronograma = form.save()  # Guarda el cronograma y obtén el objeto creado
            return redirect(
                "ver_pagos_cronograma", cronograma_id=cronograma.id
            )  # Redirige a la vista de pagos del nuevo cronograma
    else:
        form = CronogramaForm()
    return render(request, "crear_cronograma.html", {"form": form})


def ver_pagos_cronograma(request, cronograma_id):
    cronograma = get_object_or_404(Cronograma, pk=cronograma_id)
    pagos = PagoCronograma.objects.filter(cronograma=cronograma)
    return render(
        request, "ver_pagos_cronograma.html", {"cronograma": cronograma, "pagos": pagos}
    )


def pagos_cronograma(request, cronograma_id):
    pagos = PagoCronograma.objects.filter(cronograma_id=cronograma_id)
    cronograma = get_object_or_404(Cronograma, pk=cronograma_id)
    detalle_cronograma = cronograma.detalle
    return render(
        request,
        "pagos_cronograma.html",
        {"pagos": pagos, "detalle_cronograma": detalle_cronograma},
    )


def ver_cronogramas(request):
    cronogramas = Cronograma.objects.all()
    return render(request, "ver_cronogramas.html", {"cronogramas": cronogramas})


def ver_cronogramas_filtrados(request, tipo):
    if tipo == "sunat":
        cronogramas = Cronograma.objects.filter(entidad_bancaria__icontains="SUNAT")
    else:
        cronogramas = Cronograma.objects.exclude(entidad_bancaria__icontains="SUNAT")

    return render(request, "ver_cronogramas.html", {"cronogramas": cronogramas})


# metodos HTMX
@require_http_methods(["POST"])
def editar_monto_pago(request, pago_id):
    if request.method == "POST":
        pago = get_object_or_404(PagoCronograma, id=pago_id)
        nuevo_monto = request.POST.get("monto_pago")
        if nuevo_monto:
            try:
                pago.monto_pago = nuevo_monto
                pago.save()
                return HttpResponse(
                    f"<span>{pago.monto_pago}</span>"
                )  # Respuesta para htmx
            except Exception as e:
                # Manejar la excepción si es necesario
                pass
    # Redireccionar o responder de otra manera si no es una solicitud POST o si hay un error


@require_http_methods(["POST"])
def cambiar_pdf_pago(request, pago_id):
    pago = get_object_or_404(PagoCronograma, pk=pago_id)
    form = CambiarPDFPagoForm(request.POST, request.FILES, instance=pago)
    if form.is_valid():
        form.save()
        return JsonResponse({"mensaje": "PDF actualizado correctamente"})
    return JsonResponse({"error": "Datos del formulario no válidos"}, status=400)


def editar_fecha_pago(request, pago_id):
    pago = get_object_or_404(PagoCronograma, pk=pago_id)
    if request.method == "POST":
        form = EditarFechaPagoForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            # Redireccionar a donde sea apropiado después de la actualización
            return HttpResponse(
                f"<span>{pago.fecha_pago}</span>"
            )  # Respuesta para htmx
    else:
        form = EditarFechaPagoForm(instance=pago)

    return render(request, "editar_fecha_pago.html", {"form": form, "pago": pago})
