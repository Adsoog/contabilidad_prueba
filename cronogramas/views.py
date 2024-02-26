from django.shortcuts import get_object_or_404, render, redirect

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
    return render(request, 'pagos_cronograma.html', {'pagos': pagos})


def ver_cronogramas(request):
    cronogramas = Cronograma.objects.all()
    return render(request, "ver_cronogramas.html", {"cronogramas": cronogramas})


def ver_cronogramas_filtrados(request, tipo):
    if tipo == 'sunat':
        cronogramas = Cronograma.objects.filter(entidad_bancaria__icontains='SUNAT')
    else:
        cronogramas = Cronograma.objects.exclude(entidad_bancaria__icontains='SUNAT')
    
    return render(request, "ver_cronogramas.html", {"cronogramas": cronogramas})