# apps/certifications/urls.py

"""
Definição das URLs para o aplicativo Certification.
"""

from django.urls import path

from . import views


urlpatterns = [
    # URL página Principal de Certificações
    path(
        "certifications/",
        views.certification_home,
        name="certification_home"
    ),

    # URLs de Certificações
    path(
        "certification/list/",
        views.certification_list,
        name="certification_list"
    ),
    path(
        "certification/<int:pk>/",
        views.certification_detail,
        name="certification_detail"
    ),
    path(
        "certification/new/",
        views.certification_new,
        name="certification_new"
    ),
    path(
        "certification/<int:pk>/edit/",
        views.certification_edit,
        name="certification_edit"
    ),
    path(
        "certification/<int:pk>/delete/",
        views.certification_delete,
        name="certification_delete"
    ),
]
