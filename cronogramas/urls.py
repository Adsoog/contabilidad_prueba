from django.urls import path
from .views import crear_cronograma
from . import views

urlpatterns = [
    path('crear_cronograma/', crear_cronograma, name='crear_cronograma'),
    path('cronogramas/<int:cronograma_id>/ver_pagos/', views.ver_pagos_cronograma, name='ver_pagos_cronograma'),

    # Otras URLs de tu aplicación...
]
