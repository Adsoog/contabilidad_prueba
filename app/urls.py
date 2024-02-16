from django.urls import path
from . import views

urlpatterns = [
    path('list', views.index, name='index'),
    path('list_programmers/', views.list_programmers, name='list_programmers')
]
