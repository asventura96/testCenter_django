# apps/testCenter/urls.py

"""
Definição das URLs para o aplicativo TestCenter.
"""

from django.urls import path

from . import views

urlpatterns = [
    # URL página Principal do Centro de Provas
    path(
        "testcenter/",
        views.testcenter_home,
        name="testcenter_home"
    ),
    # URLs de Centros de Provas
    path("testcenter/list/", views.testcenter_list, name="testcenter_list"),
    path(
        "testcenter/<int:pk>/",
        views.testcenter_detail,
        name="testcenter_detail"
    ),
    path(
        "testcenter/new/",
        views.testcenter_new,
        name="testcenter_new"
    ),
    path(
        "testcenter/<int:pk>/edit/",
        views.testcenter_edit,
        name="testcenter_edit"
    ),
    path(
        "testcenter/<int:pk>/delete/",
        views.testcenter_delete,
        name="testcenter_delete"
    ),
]
