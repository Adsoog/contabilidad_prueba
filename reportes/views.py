from django.shortcuts import render, get_object_or_404
from ordenventa.models import OrdenVenta, ItemOrdenVenta


def reportes_registros(request):
    return render(request, 'reportes_registros.html')   

def calcular_precio_bruto_total(orden_venta):
    # Obtener todos los items relacionados con esta orden
    items = ItemOrdenVenta.objects.filter(ordenventa=orden_venta)
    # Calcular el precio bruto total sumando los precios brutos de todos los items
    precio_bruto_total = sum(item.total_bruto if item.total_bruto is not None else 0 for item in items)
    return precio_bruto_total
    

def reporte_precio_bruto_total(request, ordenventa_id=None):
    if ordenventa_id is not None:
        orden_venta = get_object_or_404(OrdenVenta, pk=ordenventa_id)
        precio_bruto_total = calcular_precio_bruto_total(orden_venta)
        return render(
            request,
            "reporte_precio_bruto_total.html",
            {"orden_venta": orden_venta, "precio_bruto_total": precio_bruto_total},
        )
    else:
        ordenes_venta = OrdenVenta.objects.all()
        return render(
            request,
            "lista_ordenes_venta.html",
            {"ordenes_venta": ordenes_venta},
        )
    
