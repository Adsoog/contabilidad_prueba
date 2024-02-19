from django.urls import path
from .views import lista_ordenes_compra, crear_orden_compra, ordenpago

urlpatterns = [
    path("", lista_ordenes_compra, name="lista_ordenes_compra"),
    path("crear_orden_compra/", crear_orden_compra, name="crear_orden_compra"),
    path("ordenpago/", ordenpago, name="ordenpago"),
]
