from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from ordenventa.models  import ItemOrdenVenta

def index(request):
    return render(request, 'ordencompra.html')

def list_items(_request):
    items = list(ItemOrdenVenta.objects.values())
    data ={'itemsordenventa': items }
    return JsonResponse(data)
