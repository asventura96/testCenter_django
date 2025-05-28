# apps/certifiers/urls.py

"""
Definição das URLs para o aplicativo Certifier.
"""

from django.urls import path

from . import views

urlpatterns = [
    # URL página Principal de Certificadores
    path("certifiers/", views.certifier_home, name="certifier_home"),
    # URLs de Certificadores
    path("certifier/list/", views.certifier_list, name="certifier_list"),
    path(
        "certifier/<int:pk>/",
        views.certifier_detail,
        name="certifier_detail"
    ),
    path("certifier/new/", views.certifier_new, name="certifier_new"),
    path(
        "certifier/<int:pk>/edit/",
        views.certifier_edit,
        name="certifier_edit"
    ),
    path(
        "certifier/<int:pk>/delete/",
        views.certifier_delete,
        name="certifier_delete"
    ),
]
