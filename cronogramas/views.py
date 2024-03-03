import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .forms import EditarFechaPagoForm, EditarMontoForm, CambiarPDFPagoForm
from .models import DetallePago, PagoCronograma, Resolucion
from cronogramas.models import Cronograma, PagoCronograma
from .forms import CronogramaForm  # Importa el formulario de Cronograma
from django.urls import reverse
import pdfplumber
import re
from django.utils.dateparse import parse_date


def crear_cronograma(request):
    if request.method == "POST":
        # Modifica esta línea para incluir request.FILES
        form = CronogramaForm(request.POST, request.FILES)
        if form.is_valid():
            cronograma = form.save()  # Guarda el cronograma y obtén el objeto creado
            return redirect("ver_pagos_cronograma", cronograma_id=cronograma.id)
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
        cronogramas = Cronograma.objects.filter(entidad__icontains="SUNAT")
    else:
        cronogramas = Cronograma.objects.exclude(entidad__icontains="SUNAT")

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
        # Asume que tienes el ID del cronograma disponible o puedes obtenerlo de `pago`
        cronograma_id = pago.cronograma.id
        return redirect(reverse("pagos_cronograma", args=[cronograma_id]))
    else:
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


# METODO CON PDF PARA SUNAT aqui abajo se veran cosas tenebrosas :()


def procesar_pdf(request):
    if request.method == "POST":
        archivo_pdf = request.FILES["archivo_pdf"]
        with pdfplumber.open(archivo_pdf) as pdf:
            texto_completo = ""
            for pagina in pdf.pages:
                texto_completo += pagina.extract_text()

        # Aquí pondrías la lógica para extraer la información del texto
        # usando expresiones regulares o cualquier otro método adecuado.
        # Por ejemplo:
        numero_resolucion = "Extraído del texto"
        tipo_resolucion = "Extraído del texto"
        tiempo_aplazamiento = 6  # Extraído del texto y convertido a entero

        # Crear el objeto Resolución
        resolucion = Resolucion.objects.create(
            numero=numero_resolucion,
            tipo_resolucion=tipo_resolucion,
            tiempo_aplazamiento=tiempo_aplazamiento,
        )

        # Suponiendo que has extraído los detalles de pago en una lista de diccionarios llamada 'detalles_pagos

        return redirect("alguna_url_despues_de_procesar")  # Redirigir a alguna parte
    else:
        return render(request, "subir_pdf.html")  # La plantilla para subir el PDF
