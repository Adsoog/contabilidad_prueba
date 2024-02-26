from django.urls import path
from .views import (
    ListaOrdenesVenta,
    DetalleOrdenVenta,
    ListaItemsOrdenVenta,
    DetalleItemOrdenVenta,
    OrdenVentaCRUDView,
    procesar_orden_venta_excel,
    ver_items_orden_venta,
    procesar_seleccion,
    ver_items_enviados_orden_venta,
    ver_items_orden_venta2,
)

urlpatterns = [
    path("ordenesventa/", ListaOrdenesVenta.as_view(), name="lista_ordenesventa"),
    path(
        "ordenesventa/<int:pk>/", DetalleOrdenVenta.as_view(), name="detalle_ordenventa"
    ),
    path(
        "itemsordenesventa/",
        ListaItemsOrdenVenta.as_view(),
        name="lista_itemsordenesventa",
    ),
    path(
        "itemsordenesventa/<int:pk>/",
        DetalleItemOrdenVenta.as_view(),
        name="detalle_itemordenventa",
    ),
    # A partir de aqui recien las funcionalidades
    path("", OrdenVentaCRUDView.as_view(), name="ordenventa-crud"),
    path("cargar-orden-venta/", procesar_orden_venta_excel, name="cargar_orden_venta"),
    path(
        "ordenventa/procesar/<int:ordenventa_id>/",
        procesar_orden_venta_excel,
        name="procesar_orden_venta_excel",
    ),
    # no lo se rick
    path(
        "ver_items_orden_venta/<int:ordenventa_id>/",
        ver_items_orden_venta,
        name="ver_items_orden_venta",
    ),
    path(
        "ver_items_orden_venta2/<int:ordenventa_id>/",
        ver_items_orden_venta2,
        name="ver_items_orden_venta2",
    ),
    path(
        "procesar_seleccion/<int:ordenventa_id>/",
        procesar_seleccion,
        name="procesar_seleccion",
    ),
]
