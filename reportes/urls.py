from django.urls import path
from .views import reporte_precio_bruto_total

urlpatterns = [
    path('ordenventa/', reporte_precio_bruto_total, name='lista_ordenes_venta'),
    path('ordenventa/<int:ordenventa_id>/', reporte_precio_bruto_total, name='reporte_precio_bruto_total'),
    # Otras URLS de tu aplicación de reportes, si las tienes...
]
