from django.urls import path
from .views import crear_cronograma, ver_cronogramas_filtrados
from . import views

urlpatterns = [
    path("crear_cronograma/", crear_cronograma, name="crear_cronograma"),
    path(
        "cronogramas/<int:cronograma_id>/ver_pagos/",
        views.ver_pagos_cronograma,
        name="ver_pagos_cronograma",
    ),
    path("ver_cronogramas/", views.ver_cronogramas, name="ver_cronogramas"),
    path(
        "cronogramas/<int:cronograma_id>/pagos/",
        views.pagos_cronograma,
        name="pagos_cronograma",
    ),
    # Otras URLs de tu aplicación...
    path(
        "cronogramas/<str:tipo>/",
        ver_cronogramas_filtrados,
        name="ver_cronogramas_filtrados",
    ),
    # hmtx urls
    path(
        "editar_monto/<int:pago_id>/", views.editar_monto_pago, name="editar_monto_pago"
    ),
    path("cambiar_pdf/<int:pago_id>/", views.cambiar_pdf_pago, name="cambiar_pdf_pago"),
    path(
        "editar-fecha/<int:pago_id>/", views.editar_fecha_pago, name="editar_fecha_pago"
    ),
]
