from django.urls import path
from .views import reporte_precio_bruto_total
from reportes import views

urlpatterns = [
    path('ordenventa/', reporte_precio_bruto_total, name='lista_ordenes_venta'),
    path('ordenventa/<int:ordenventa_id>/', reporte_precio_bruto_total, name='reporte_precio_bruto_total'),
    path('reportes/', views.reportes_registros, name='ruta_reportes'),
    # Otras URLS de tu aplicación de reportes, si las tienes...



    #proveedores:
    path('proveedores/', views.ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/nuevo/', views.ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedores/editar/<int:pk>/', views.ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('proveedores/eliminar/<int:pk>/', views.ProveedorDeleteView.as_view(), name='proveedor_delete'),
]
