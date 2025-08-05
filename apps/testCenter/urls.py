# apps/testCenter/urls.py

"""
Definição das URLs para o aplicativo TestCenter.
"""

from django.urls import path

from . import views

urlpatterns = [
    # URL página Principal do Centro de Provas
    path(
        "testCenter/",
        views.testcenter_home,
        name="testcenter_home"
    ),

    # URLs de Centros de Provas
    path("testCenter/list/", views.testcenter_list, name="testcenter_list"),
    path(
        "testCenter/<int:pk>/",
        views.testcenter_detail,
        name="testcenter_detail"
    ),
    path(
        "testCenter/new/",
        views.testcenter_new,
        name="testcenter_new"
    ),
    path(
        "testCenter/<int:pk>/edit/",
        views.testcenter_edit,
        name="testcenter_edit"
    ),
    path(
        "testCenter/<int:pk>/delete/",
        views.testcenter_delete,
        name="testcenter_delete"
    ),

    # URLs de Exames Realizados no Centro de Provas
    path(
        "exams/",
        views.exam_list,
        name="exam_list"
    ),
]
