# apps/clients/urls.py

"""
Definição das URLs para o aplicativo Client.
"""

from django.urls import path
from . import views

urlpatterns = [
    # URL página Principal de Clientes
    path("clients/", views.client_home, name="client_home"),
    # URLs de Clientes
    path("client/new/", views.client_new, name="client_new"),
    path("client/list/", views.client_list, name="client_list"),
    path("client/<int:pk>/", views.client_detail, name="client_detail"),
    path("client/<int:pk>/edit/", views.client_edit, name="client_edit"),
    path("client/<int:pk>/delete/", views.client_delete, name="client_delete"),
]
