from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView
from django.views.decorators.http import require_http_methods, require_POST
from django.urls import reverse
from django.utils.dateparse import parse_date
from .forms import (
    EditarFechaPagoForm,
    EditarMontoForm,
    CambiarPDFPagoForm,
    PDFUploadForm,
    PagoForm,
    CronogramaForm,
)
from .models import DetallePago, PagoCronograma, Resolucion, Pago
from cronogramas.models import Cronograma
from django.utils import timezone

import pdfplumber
import re
from datetime import date, datetime, timedelta

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


# METODO CON PDF PARA SUNAT aqui abajo se veran cosas tenebrosas :O
def cargar_pdf(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_pdf = request.FILES["archivo_pdf"]
            texto_completo = ""
            with pdfplumber.open(archivo_pdf) as pdf:
                for pagina in pdf.pages:
                    texto_completo += pagina.extract_text()

            # Extracción de datos del PDF
            # (La lógica de extracción de datos aquí sigue siendo la misma)
            # Extracción de datos del PDF
            regex_resolucion = r"RESOLUCIÓN DE INTENDENCIA N.° (\d+)"
            regex_aplazamiento = r"(Aplazamiento con Fraccionamiento|Fraccionamiento|Aplazamiento) por (\d+) mes\(es\)"
            regex_tabla = r"([A-Z]+|\d+)\s(\d{2}\/\d{2}\/\d{4})\s([\d,\.]+)\s([\d,\.]+)\s([\d,\.]+)\s([\d,\.]+)"

            numero_resolucion = re.search(regex_resolucion, texto_completo)
            if numero_resolucion:
                numero_resolucion = numero_resolucion.group(1)
            else:
                numero_resolucion = "No encontrado"

            match_aplazamiento = re.search(regex_aplazamiento, texto_completo)
            if match_aplazamiento:
                tipo_resolucion = match_aplazamiento.group(1)
                tiempo_aplazamiento = match_aplazamiento.group(2)
            else:
                tipo_resolucion = "No especificado"
                tiempo_aplazamiento = "No encontrado"

            # Nueva lógica para extraer descripción, monto del tributo, interés y total
            patron = r"(\d{6})\s+(\d{4})\s+(.+?)\s+(\d{3}\d{3}\d{7}\d{4})\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)"
            coincidencias = re.findall(patron, texto_completo, re.DOTALL)
            if coincidencias:
                # Asumiendo que solo quieres la última coincidencia para llenar los campos de la resolución
                descripcion, monto_tributo, interes, total = coincidencias[-1]
                # Ajustar la descripción
                descripcion = " ".join(
                    descripcion.split()[:-1]
                )  # Remueve el número de documento al final, si es necesario
            else:
                # Valores predeterminados en caso de que no se encuentren coincidencias
                descripcion = "Descripción no encontrada"
                monto_tributo = "0"  # Asigna un valor de cadena en lugar de entero
                interes = "0"  # Asigna un valor de cadena
                total = "0"  # Asigna un valor de cadena

            coincidencias_tabla = re.findall(regex_tabla, texto_completo)
            datos_tabla = [
                {
                    "numero_cuota": fila[0],
                    "Vencimiento": fila[1],
                    "Amortización": fila[2],
                    "Interés": fila[3],
                    "Total": fila[4],
                    "Saldo": fila[5],
                }
                for fila in coincidencias_tabla
            ]

            # Guardar los datos de la resolución en la base de datos
            resolucion_obj = Resolucion(
                numero_resolucion=(
                    numero_resolucion if numero_resolucion != "No encontrado" else None
                ),
                tipo_resolucion=tipo_resolucion,
                tiempo_aplazamiento=tiempo_aplazamiento,
                descripcion=descripcion,  # Nuevo campo
                monto_tributo=Decimal(monto_tributo.replace(",", "")),
                interes=Decimal(interes.replace(",", "")),
                total=Decimal(total.replace(",", "")),
                archivo_pdf=archivo_pdf,
            )
            resolucion_obj.save()

            # Guardar los datos de la tabla de pagos
            for fila in datos_tabla:
                Pago.objects.create(
                    resolucion=resolucion_obj,
                    numero_cuota=fila["numero_cuota"],
                    vencimiento=datetime.strptime(
                        fila["Vencimiento"], "%d/%m/%Y"
                    ).date(),
                    amortizacion=Decimal(fila["Amortización"].replace(",", "")),
                    interes=Decimal(fila["Interés"].replace(",", "")),
                    total=Decimal(fila["Total"].replace(",", "")),
                    saldo=Decimal(fila["Saldo"].replace(",", "")),
                )

            # Redirigir al usuario a una página de confirmación o de resumen después del guardado
            return redirect(
                "lista_resoluciones"
            )  # Asegúrate de reemplazar 'url_a_confirmacion' con la URL real

    else:
        form = PDFUploadForm()
    return render(request, "cargar_pdf.html", {"form": form})


# vistas de cronogramas sunat
class ResolucionListView(ListView):
    model = Resolucion
    context_object_name = "resoluciones"
    template_name = "resolucion_list.html"


@require_POST  # Asegura que esta vista solo pueda ser accedida mediante un método POST
def eliminar_resolucion(request, pk):
    resolucion = get_object_or_404(Resolucion, pk=pk)
    resolucion.delete()
    messages.success(request, "Resolución eliminada con éxito.")
    return redirect(reverse("lista_resoluciones"))


def detalle_resolucion(request, pk):
    resolucion = get_object_or_404(Resolucion, pk=pk)
    pagos = Pago.objects.filter(resolucion=resolucion)

    # No necesitas manejar el método POST ni el formulario en esta vista
    return render(
        request,
        "detalle_resolucion.html",
        {
            "resolucion": resolucion,
            "pagos": pagos,
        },
    )


def cambiar_pdf_pago_sunat(request, pk):
    if request.method == "POST":
        pago = get_object_or_404(Pago, pk=pk)
        form = PagoForm(request.POST, request.FILES, instance=pago)
        if form.is_valid():
            form.save()
            # Retorna algo adecuado para htmx, por ejemplo, un enlace al nuevo PDF
            return HttpResponse(
                f'<a href="{pago.pago_sunat.url}" target="_blank">Ver Documento</a>'
            )
    # Manejar caso de error o solicitud no POST
    return HttpResponse("Operación no permitida", status=405)


#### CRONOGRAMA SEMAFORO
from datetime import date, timedelta

def cronograma_semaforo(request):
    pagos = Pago.objects.filter(vencimiento__gte=date.today()).order_by('vencimiento')
    hoy = date.today()
    proximo = hoy + timedelta(days=30)  # Ajusta este valor según tus necesidades

    # Obtener la fecha y hora actuales en la zona horaria definida en settings.py
    ahora = timezone.localtime(timezone.now())

    for pago in pagos:
        if pago.vencimiento < hoy:
            pago.estado_clase = 'table-danger'  # Pago vencido
        elif pago.vencimiento <= proximo:
            pago.estado_clase = 'table-warning'  # Próximo vencimiento
        else:
            pago.estado_clase = 'table-success'  # Vencimiento más lejano

    return render(request, 'semaforo.html', {
        'pagos': pagos,
        'ahora': ahora,  # Pasar la fecha y hora actuales al contexto
    })
