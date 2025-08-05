# apps/testCenter/views.py

"""
Definição das views para o aplicativo TestCenter.
"""

from datetime import datetime, timedelta

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError, DatabaseError
from django.db.models import Q, ProtectedError
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.utils.json_responses import json_error_response, log_exception

from .forms import TestCenterForm, TestCenterExamForm
from .models import TestCenter, TestCenterExam, Certification, Client


def testcenter_home(request):
    """View para a página inicial de Centros de Provas."""
    return render(
        request,
        "testCenters/testCenters_home.html"
    )


def testcenter_list(request):
    """View para listar os Centros de Provas."""

    # Obtenção dos Filtros
    query = request.GET.get("testCenter-list-query")
    idle = request.GET.get("testCenter-list-idle")

    # Ordenação
    order_by = request.GET.get("order_by", "name")
    descending = request.GET.get("descending", "False") == "True"

    # Otimização da Consulta
    testcenter = TestCenter.objects.all()

    # Filtragem
    if query:
        testcenter = testcenter.filter(
            Q(name__icontains=query)
        )

    if idle in ["True", "False"]:
        testcenter = testcenter.filter(idle=(idle == "True"))

    # Aplicação de Filtros da Ordenação
    if descending:
        order_by = f"-{order_by}"
    testcenter = testcenter.order_by(order_by)

    # Registros por Página
    records_per_page = request.GET.get("records_per_page", 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 10

    # Paginação
    paginator = Paginator(testcenter, records_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Tratamento de Erros na Paginação
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Definição dos Campos de Pesquisa
    search_fields = [
        {
            "id": "testCenter-list-query",
            "name": "testCenter-list-query",
            "label": "Busque pelo Nome",
            "placeholder": "Digite o Nome do Centro de Provas",
            "type": "text",
            "value": request.GET.get("q", ""),
        },
        {
            "id": "testCenter-list-idle",
            "name": "testCenter-list-idle",
            "label": "Centro de Provas Inativo?",
            "type": "select",
            "options": [("True", "Sim"), ("False", "Não")],
            "selected": request.GET.get("idle", ""),
        },
    ]

    context = {
        "testcenter": testcenter,
        "page_obj": page_obj,
        "search_fields": search_fields,
        "query_params": request.GET.urlencode(),
        "headers": [
            {"field": "id", "label": "ID"},
            {"field": "name", "label": "Nome"},
            {"field": "notes", "label": "Observações"},
            {"field": "idle", "label": "Inativo"},
        ],
        "rows": [
            [
                testcenter.id,
                mark_safe(
                    f'<a href="{reverse(
                        "testcenter_detail",
                        args=[testcenter.id]
                    )}">{testcenter.name}</a>'
                ),
                testcenter.notes if testcenter.notes else "",
                "Sim" if testcenter.idle else "Não",
            ]
            for testcenter in page_obj
        ],
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "includes/table.html", context)
    else:
        return render(request, "testCenters/testCenters_list.html", context)


def testcenter_detail(request, pk):
    """View para exibir os detalhes de um Centro de Provas."""

    # Obtenção dos Filtros
    testcenter = get_object_or_404(TestCenter, pk=pk)

    # Mensagem de confirmação de exclusão do Centro de Provas
    message_confirmation_delete = (
        f'Tem certeza que deseja excluir o Centro de Provas <br>'
        f'<strong>{testcenter.name}</strong>?'
    )

    # Preparação dos Dados para o template reutilizável
    tabs = [
        {
            "id": "testCenter-detail-dados",
            "class": "btn-detail",
            "label": "Detalhes",
        },
    ]

    sections = [
        {
            "id": "testCenter-detail-dados",
            "title": "Detalhes do Centro de Provas",
            "active": True,
            "fields": [
                {
                    "label": "Status do Centro de Provas",
                    "value": "Inativo" if testcenter.idle else "Ativo",
                    "label_class": "apps-detail-status-label",
                    "value_class": "apps-detail-status-value",
                },
                {
                    "label": "Nome do Centro de Provas",
                    "value": testcenter.name
                },
                {
                    "label": "Observações deste Centro de Provas",
                    "value": testcenter.notes if testcenter.notes else "",
                },
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-edit",
            "url": reverse("testcenter_edit", args=[testcenter.pk]),
            "title": "Editar Centro de Provas",
            "aria-label": "Editar Centro de Provas",
        },
        {
            "class": "btn-delete",
            "url": reverse("testcenter_delete", args=[testcenter.pk]),
            "data": {
                "model": "TestCenter",
                "pk": testcenter.pk,
                "redirect-url": reverse("testcenter_list"),
            },
            "title": "Excluir Centro de Provas",
            "aria-label": "Excluir Centro de Provas",
        },
        {
            "class": "btn-return",
            "url": reverse("testcenter_list"),
            "title": "Voltar para a lista de Centros de Provas",
            "aria-label": "Voltar para a lista de Centros de Provas",
        },
    ]

    # Renderização do template
    return render(
        request,
        "testCenters/testCenters_detail.html",
        {
            "testcenter": testcenter,
            "tabs": tabs,
            "sections": sections,
            "buttons": buttons,
            "message_confirmation_delete": message_confirmation_delete,
        },
    )


def testcenter_new(request):
    """View para adicionar um Centro de Provas."""

    if request.method == "POST":
        form = TestCenterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    "Centro de Provas adicionado com sucesso!"
                )
                return redirect(reverse("testcenter_list"))
            except IntegrityError:
                messages.error(
                    request,
                    "Erro: Já existe um Centro de Provas com este nome."
                )
            except DatabaseError as e:
                log_exception(
                    exception=e,
                    context="Erro ao adicionar o Centro de Provas",
                )
                messages.error(
                    request,
                    "Erro interno ao adicionar o Centro de Provas. "
                )
        else:
            messages.error(
                request,
                "Erro ao adicionar o Centro de Provas."
            )
    else:
        form = TestCenterForm()

    # Definição das Seções e Botões para o Template
    sections = [
        {
            "title": "Dados do Centro de Provas",
            "fields": [
                form["name"],
                form["notes"],
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-return",
            "url": reverse("testcenter_list"),
            "title": "Retornar",
            "text": "Retornar",
        },
    ]

    # Renderização do Template
    return render(
        request,
        "testCenters/testCenters_form.html",
        {
            "form": form,
            "sections": sections,
            "buttons": buttons,
        },
    )


def testcenter_edit(request, pk):
    """View para editar um Centro de Provas."""

    # Obtenção do objeto pelo ID (pk) ou retorno de erro 404 se não encontrado
    testcenter = get_object_or_404(TestCenter, pk=pk)

    # Verificação da Requisição do tipo POST
    if request.method == "POST":
        form = TestCenterForm(request.POST, instance=testcenter)

        # Validação do Formulário
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    "Centro de Provas atualizado com sucesso!"
                )
                return redirect(reverse("testcenter_list"))
            except IntegrityError:
                messages.error(
                    request,
                    "Erro: Já existe um Centro de Provas com este nome."
                )
            except DatabaseError as e:
                log_exception(
                    exception=e,
                    context="Erro ao atualizar o Centro de Provas",
                )
                messages.error(
                    request,
                    "Erro interno ao atualizar o Centro de Provas. "
                )
        else:
            messages.error(
                request,
                "Erro ao atualizar o Centro de Provas."
            )
    else:
        form = TestCenterForm(instance=testcenter)

    # Definição das Seções e Botões para o Template
    sections = [
        {
            "title": "Dados do Centro de Provas",
            "fields": [
                form["idle"],
                form["name"],
                form["notes"],
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-return",
            "url": reverse("testcenter_list"),
            "title": "Retornar",
            "text": "Retornar",
        },
    ]

    # Renderização do Template
    return render(
        request,
        "testCenters/testCenters_form.html",
        {
            "form": form,
            "sections": sections,
            "buttons": buttons,
        },
    )


def testcenter_delete(request, pk):
    """View para excluir um Centro de Provas."""

    # Obtenção do objeto pelo ID (pk) ou retorno de erro 404 se não encontrado
    testcenter = get_object_or_404(TestCenter, pk=pk)

    # Mensagem de confirmação de exclusão do Centro de Provas
    message_confirmation_delete = (
        f'Tem certeza que deseja excluir o Centro de Provas <br>'
        f'<strong>{testcenter.name}</strong>?'
    )

    # Verificação da Requisição do tipo POST
    if request.method == "POST":
        try:
            testcenter.delete()
            messages.success(
                request,
                (
                    f'O Centro de Provas "<strong>{testcenter.name}</strong>" '
                    f'foi excluído com sucesso!'
                )
            )
            return JsonResponse({
                "success": True,
                "message": (
                    f'O Centro de Provas "<strong>{testcenter.name}</strong>" '
                    f'foi excluído com sucesso!'
                )
            })
        except ProtectedError:
            return JsonResponse({
                "success": False,
                "message": (
                    "Não é possível excluir o Centro de Provas porque "
                    "ele está relacionado a outros registros."
                )
            })
        except (IntegrityError, DatabaseError) as e:
            return json_error_response(
                message_user="Erro ao excluir o Centro de Provas.",
                exception=e,
                context=f"Exclusão de Centro de Provas {testcenter.pk}"
            )
        except ValidationError as e:
            return json_error_response(
                message_user=(
                    "Erro de validação ao excluir o Centro de Provas."
                ),
                exception=e,
                level="warning",
                context=(
                    f"Validação ao excluir Centro de Provas {testcenter.pk}"
                )
            )

    # Renderização do Template
    return render(
        request,
        "testcenters/testcenters_confirmDelete.html",
        {
            "testcenter": testcenter,
            "message_confirmation_delete": message_confirmation_delete,
        }
    )


def exam_list(request):
    """View para listar os Exames Realizados no Centro de Provas."""

    # Obtenção dos Filtros
    client = request.GET.get("exam-list-client")
    certification = request.GET.get("exam-list-certification")
    test_center = request.GET.get("exam-list-testCenter")
    date_range = request.GET.get("exam-list-dateRange")
    presence = request.GET.get("exam-list-presence")

    # Ordenação
    order_by = request.GET.get("order_by", "date")
    descending = request.GET.get("descending", "False") == "True"

    # Otimização da Consulta
    exams = TestCenterExam.objects.select_related(
        "client",
        "test_center",
        "certification",
    )

    # Filtragem
    if client:
        exams = exams.filter(client__uid=client)

    if certification:
        exams = exams.filter(certification__id=certification)

    if test_center:
        exams = exams.filter(testCenter__id=test_center)

    if date_range:
        try:
            start_date, end_date = date_range.split(" - ")
            start_date = datetime.strptime(
                start_date.strip(),
                '%d/%m/%Y'
            ).date()
            end_date = datetime.strptime(
                end_date.strip(),
                '%d/%m/%Y'
            ).date()
            end_date += timedelta(days=1)  # Inclui o final do dia
            exams = exams.filter(date__range=[start_date, end_date])
        except (ValueError, TypeError):
            pass

    if presence in ["True", "False"]:
        exams = exams.filter(presence=(presence == "True"))

    # Aplicação de Filtros da Ordenação
    if descending:
        order_by = f"-{order_by}"
        exams = exams.order_by(order_by)

    # Registros por Página
    records_per_page = request.GET.get("records_per_page", 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 10

    # Paginação
    paginator = Paginator(exams, records_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Tratamento de Erros na Paginação
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Busca e Ordenação das Opções de Seleção
    clients = Client.objects.order_by("name")
    certifications = Certification.objects.order_by("name")
    test_centers = TestCenter.objects.order_by("name")

    # Definição dos Campos de Pesquisa
    search_fields = [
        {
            "type": "daterange",
            "id": "exam-list-dateRange",
            "name": "exam-list-dateRange",
            "label": "Período de Realização do Exame",
            "value": request.GET.get("date_range", ""),
        },
        {
            "id": "exam-list-client",
            "name": "exam-list-client",
            "label": "Cliente",
            "type": "select",
            "options": [
                (
                    client.uid,
                    f"{client.uid}: {client.name}"
                ) for client in clients
            ],
            "selected": request.GET.get("client", ""),
        },
        {
            "id": "exam-list-certification",
            "name": "exam-list-certification",
            "label": "Certificação",
            "type": "select",
            "options": [
                (
                    certification.id,
                    f"{certification.name}({certification.examCode})"
                ) for certification in certifications
            ],
            "selected": request.GET.get("certification", ""),
        },
        {
            "id": "exam-list-testCenter",
            "name": "exam-list-testCenter",
            "label": "Centro de Provas",
            "type": "select",
            "options": [
                (
                    test_center.id,
                    test_center.name
                ) for test_center in test_centers
            ],
            "selected": request.GET.get("test_center", ""),
        },
        {
            "id": "exam-list-presence",
            "name": "exam-list-presence",
            "label": "Presença Confirmada?",
            "type": "select",
            "options": [("True", "Sim"), ("False", "Não")],
            "selected": request.GET.get("presence", ""),
        },
    ]

    context = {
        "exams": exams,
        "page_obj": page_obj,
        "search_fields": search_fields,
        "query_params": request.GET.urlencode(),
        "headers": [
            {"field": "date", "label": "Data e Hora do Exame"},
            {"field": "client__name", "label": "Cliente"},
            {"field": "certification__name", "label": "Certificação"},
            {"field": "test_center__name", "label": "Centro de Provas"},
            {"field": "presence", "label": "Presença Confirmada"},
            {"field": "notes", "label": "Observações"},
        ],
        "rows": [
            [
                timezone.localtime(exam.date).strftime("%d/%m/%Y %H:%M"),
                mark_safe(
                    f'<a href="{reverse(
                        "exam_detail",
                        args=[exam.id]
                    )}">'
                    f'{exam.client.name if exam.client else ""}</a>'
                ),
                exam.certification.name if exam.certification else "",
                exam.test_center.name if exam.test_center else "",
                "Sim" if exam.presence else "Não",
            ]
            for exam in page_obj
        ],
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "includes/table.html", context)
    else:
        return render(request, "testCenters/exams_list.html", context)


def exam_detail(request, pk):
    """
    View para exibir os detalhes de um Exame Realizado no Centro de Provas.
    """

    # Obtenção dos Filtros
    exam = get_object_or_404(TestCenterExam, pk=pk)

    # Mensagem de confirmação de exclusão do Exame
    message_confirmation_delete = (
        f'Tem certeza que deseja excluir o Exame <br>'
        f'<strong>{exam.client.name} - {exam.certification.name}</strong>?'
    )

    # Preparação dos Dados para o template reutilizável
    tabs = [
        {
            "id": "exam-detail-dados",
            "class": "btn-detail",
            "label": "Detalhes",
        },
    ]

    sections = [
        {
            "id": "exam-detail-dados",
            "title": "Detalhes do Exame Realizado no Centro de Provas",
            "active": True,
            "fields": [
                {
                    "label": "ID do Exame",
                    "value": exam.id,
                    "label_class": "apps-detail-id-label",
                    "value_class": "apps-detail-id-value",
                },
                {
                    "label": "Data e Hora do Exame",
                    "value": exam.date if exam.date else "",
                    "label_class": "apps-detail-date-label",
                    "value_class": "apps-detail-date-value",
                },
                {
                    "label": "Cliente",
                    "value": (
                        f"{exam.client.uid}: {exam.client.name}"
                        if exam.client
                        else "-"
                    ),
                },
                {
                    "label": "Certificação",
                    "value": (
                        exam.certification.name
                        if exam.certification
                        else ""
                    ),
                },
                {
                    "label": "Centro de Provas",
                    "value": (
                        exam.test_center.name
                        if exam.test_center
                        else ""
                    ),
                },
                {
                    "label": "Presença Confirmada?",
                    "value": "Sim" if exam.presence else "Não",
                },
                {
                    "label": "Observações deste Exame",
                    "value": exam.notes if exam.notes else "",
                },
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-edit",
            "url": reverse("exam_edit", args=[exam.pk]),
            "title": "Editar Exame Realizado no Centro de Provas",
            "aria-label": "Editar Exame Realizado no Centro de Provas",
        },
        {
            "class": "btn-delete",
            "url": reverse("exam_delete", args=[exam.pk]),
            "data": {
                "model": "TestCenterExam",
                "pk": exam.pk,
                "redirect-url": reverse("exam_list"),
            },
            "title": "Excluir Exame Realizado no Centro de Provas",
            "aria-label": "Excluir Exame Realizado no Centro de Provas",
        },
        {
            "class": "btn-return",
            "url": reverse("exam_list"),
            "title": (
                "Voltar para a lista de Exames Realizados no Centro de Provas"
            ),
            "aria-label": (
                "Voltar para a lista de Exames Realizados no Centro de Provas"
            ),
        },
    ]

    # Renderização do template
    return render(
        request,
        "testCenters/exams_detail.html",
        {
            "exam": exam,
            "tabs": tabs,
            "sections": sections,
            "buttons": buttons,
            "message_confirmation_delete": message_confirmation_delete,
        },
    )
