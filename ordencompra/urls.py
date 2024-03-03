from django.urls import path

from ordenventa.views import ver_ordenes_pago
from .views import (
    lista_ordenes_venta,
    detalle_orden_compra,
    lista_ordenes_compra2,
    crear_orden_compra,
    ordenpago,
)

urlpatterns = [
    path("listascreo", lista_ordenes_compra2, name="lista_ordenes_compra"),
    path("crear_orden_compra/", crear_orden_compra, name="crear_orden_compra"),
    path("ordenpago/", ordenpago, name="ordenpago"),
    path("", lista_ordenes_venta, name="lista_ordenes_venta"),
    path(
        "orden_compra/<int:pk>/ordenes_compra/",
        detalle_orden_compra,
        name="detalle_orden_compra",
    ),
    path(
        "ordenes-pago/<int:ordenventa_id>/", ver_ordenes_pago, name="ver_ordenes_pago"
    ),
    path(
        "ordenes-pago/filtrar/", ver_ordenes_pago, name="filtrar_ordenes_pago_por_fecha"
    ),
]
