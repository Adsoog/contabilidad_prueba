from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ordencompra'),
    path('list_items/', views.list_items, name='list_items')
]