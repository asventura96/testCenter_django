# apps/certifications/views.py

"""
Definição das views para o aplicativo Certification.
"""

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError, DatabaseError
from django.db.models import Q, ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.utils.json_responses import json_error_response, log_exception

from .forms import CertificationForm
from .models import Certification, Certifier


def certification_home(request):
    """View para a página inicial de Certificações."""

    return render(request, "certifications/certifications_home.html")


def certification_list(request):
    """View para Listar as Certificações."""

    # Obtenção dos Filtros
    query = request.GET.get("certification-list-query")
    certifier = request.GET.get("certification-list-certifier")
    idle = request.GET.get("certification-list-idle")

    # Ordenação
    order_by = request.GET.get("order_by", "name")
    descending = request.GET.get("descending", "False") == "True"

    # Otimização da Consulta
    certification = Certification.objects.select_related("certifier")

    # Filtragem
    if query:
        certification = certification.filter(
            Q(name__icontains=query) |
            Q(examCode__icontains=query)
        )

    if certifier:
        certification = certification.filter(certifier__id=certifier)

    if idle in ["True", "False"]:
        certification = certification.filter(idle=(idle == "True"))

    # Aplicação dos Filtros da Ordenação
    if descending:
        order_by = f"-{order_by}"
    certification = certification.order_by(order_by)

    # Registros por Página
    records_per_page = request.GET.get("records_per_page", 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 10

    # Paginação
    paginator = Paginator(certification, records_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Tratamento de Erros na Paginação
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Busca e Ordenação das Opções de Seleção
    certifiers = Certifier.objects.order_by("name")

    # Definição dos Campos de Pesquisa
    search_fields = [
        {
            "id": "certification-list-query",
            "name": "certification-list-query",
            "label": "Busque pelo Nome ou Código do Exame",
            "placeholder": "Digite o Nome ou Código do Exame",
            "type": "text",
            "value": request.GET.get("q", ""),
        },
        {
            "id": "certification-list-certifier",
            "name": "certification-list-certifier",
            "label": "Selecione o Certificador",
            "type": "select",
            "options": [
                (certifier.id, f"{certifier.name} ({certifier.abbreviation})")
                for certifier in certifiers
            ],
            "selected": request.GET.get("certifier", ""),
        },
        {
            "id": "certification-list-idle",
            "name": "certification-list-idle",
            "label": "Certificação Inativa?",
            "type": "select",
            "options": [("True", "Sim"), ("False", "Não")],
            "selected": request.GET.get("idle", ""),
        },
    ]

    context = {
        "certification": certification,
        "page_obj": page_obj,
        "search_fields": search_fields,
        "query_params": request.GET.urlencode(),
        "headers": [
            {"field": "id", "label": "ID"},
            {"field": "name", "label": "Nome da Certificação"},
            {"field": "certifier", "label": "Certificador"},
            {"field": "examCode", "label": "Código do Exame"},
            {"field": "duration", "label": "Duração (minutos)"},
            {"field": "notes", "label": "Observações"},
            {"field": "idle", "label": "Inativo"},
        ],
        "rows": [
            [
                certification.id,
                mark_safe(
                    f'<a href="{reverse(
                        "certification_detail",
                        args=[certification.id]
                    )}">{certification.name}</a>'
                ),
                certification.certifier.name,
                certification.examCode,
                certification.duration,
                certification.notes,
                "Sim" if certification.idle else "Não",
            ]
            for certification in page_obj
        ],
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "includes/table.html", context)
    else:
        return render(
            request,
            "certifications/certifications_list.html",
            context
        )


def certification_detail(request, pk):
    """View para Visualizar os Detalhes de uma Certificação."""

    # Obtenção dos Filtros
    certification = get_object_or_404(Certification, pk=pk)

    # Mensagem de confirmação de exclusão do Certificador
    message_confirmation_delete = (
        f'Tem certeza que deseja excluir a Certificação <br>'
        f'<strong>{certification.name}</strong>?'
    )

    # Preparação dos Dados para o template reutilizável
    tabs = [
        {
            "id": "certification-detail-dados",
            "class": "btn-detail",
            "label": "Detalhes",
        },
    ]

    sections = [
        {
            "id": "certification-detail-dados",
            "title": "Detalhes da Certificação",
            "active": True,
            "fields": [
                {
                    "label": "Status da Certificação",
                    "value": "Inativo" if certification.idle else "Ativo",
                    "label_class": "apps-detail-status-label",
                    "value_class": "apps-detail-status-value",
                },
                {
                    "label": "Nome da Certificação",
                    "value": certification.name
                    if certification.name
                    else "-",
                },
                {
                    "label": "Nome do Certificador",
                    "value": (
                        f"{certification.certifier.name} "
                        f"({certification.certifier.abbreviation})"
                        if certification.certifier
                        else "-"
                    ),
                },
                {
                    "label": "Código do Exame",
                    "value": certification.examCode
                    if certification.examCode
                    else "-",
                },
                {
                    "label": "Duração (minutos)",
                    "value": (
                        certification.duration
                        if certification.duration is not None
                        else "-"
                    ),
                },
                {
                    "label": "Observações",
                    "value": (
                        certification.notes
                        if certification.notes
                        else ""
                    ),
                },
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-edit",
            "url": reverse("certification_edit", args=[certification.pk]),
            "title": "Editar Certificação",
            "aria-label": "Editar Certificação",
        },
        {
            "class": "btn-delete",
            "url": reverse("certification_delete", args=[certification.pk]),
            "data": {
                "model": "Certification",
                "pk": certification.pk,
                "redirect-url": reverse("certification_list"),
            },
            "title": "Excluir Certificação",
            "aria-label": "Excluir Certificação",
        },
        {
            "class": "btn-return",
            "url": reverse("certification_list"),
            "title": "Voltar para a lista de Certificações",
            "aria-label": "Voltar para a lista de Certificações",
        },
    ]

    # Renderização do Template
    return render(
        request,
        "certifications/certifications_detail.html",
        {
            "certification": certification,
            "tabs": tabs,
            "sections": sections,
            "buttons": buttons,
            "message_confirmation_delete": message_confirmation_delete,
        },
    )


def certification_new(request):
    """View para Adicionar uma Certificação."""

    if request.method == "POST":
        form = CertificationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    "Certificação adicionada com sucesso!"
                )
                return redirect("certification_list")
            except IntegrityError:
                messages.error(
                    request,
                    "Erro: Já existe uma Certificação com este ID."
                )
            except DatabaseError as e:
                log_exception(
                    exception=e,
                    context="Erro ao salvar Certificação",
                )
                messages.error(
                    request,
                    "Erro interno ao adicionar Certificação."
                )
        else:
            messages.error(
                request,
                "Erro ao adicionar Certificação."
            )
    else:
        form = CertificationForm()

    # Definição das Seções e Botões para o Template
    sections = [
        {
            "title": "Dados da Certificação",
            "fields": [
                form["certifier"],
                form["name"],
                form["examCode"],
                form["duration"],
                form["notes"],
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-return",
            "url": reverse("certification_list"),
            "title": "Retornar",
            "text": "Retornar",
        },
    ]

    # Renderização do Template
    return render(
        request,
        "certifications/certifications_form.html",
        {
            "form": form,
            "sections": sections,
            "buttons": buttons,
        },
    )


def certification_edit(request, pk):
    """View para Editar uma Certificação"""

    # Obtenção do objeto pelo ID (pk) ou retorno 404 se não encontrado
    certification = get_object_or_404(Certification, pk=pk)

    # Verificação da Requisição do tipo POST
    if request.method == "POST":
        form = CertificationForm(request.POST, instance=certification)

        # Validação do Formulário
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    "Certificação atualizada com sucesso!"
                )
                return redirect("certification_list")
            except IntegrityError:
                messages.error(
                    request,
                    "Erro: Já existe uma Certificação com este ID."
                )
            except DatabaseError as e:
                log_exception(
                    exception=e,
                    context="Erro ao atualizar Certificação",
                )
                messages.error(
                    request,
                    "Erro interno ao atualizar Certificação."
                )
        else:
            messages.error(
                request,
                "Erro ao atualizar Certificação."
            )
    else:
        form = CertificationForm(instance=certification)

    # Definição das Seções e Botões para o Template
    sections = [
        {
            "title": "Dados da Certificação",
            "fields": [
                form["idle"],
                form["certifier"],
                form["name"],
                form["examCode"],
                form["duration"],
                form["notes"],
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-return",
            "url": reverse("certification_list"),
            "title": "Retornar",
            "text": "Retornar",
        },
    ]

    # Renderização do Template
    return render(
        request,
        "certifications/certifications_form.html",
        {
            "form": form,
            "sections": sections,
            "buttons": buttons,
        },
    )


def certification_delete(request, pk):
    """View para Excluir uma Certificação."""

    # Obtenção do objeto pelo ID (pk) ou retorno de erro 404 se não encontrado
    certification = get_object_or_404(Certification, pk=pk)

    # Mensagem de confirmação de exclusão do cliente
    message_confirmation_delete = (
        f'Tem certeza que deseja excluir a Certificação <br>'
        f'<strong>{certification.name}</strong>?'
    )

    # Verificação da Requisição do tipo POST
    if request.method == "POST":
        try:
            certification.delete()
            messages.success(
                request,
                (
                    f'A Certificação "<strong>{certification.name}</strong>" '
                    f'foi excluída com sucesso!'
                )
            )
            return JsonResponse({
                "success": True,
                "message": (
                    f'A Certificação "<strong>{certification.name}</strong>" '
                    f'foi excluída com sucesso!'
                )
            })
        except ProtectedError:
            return JsonResponse({
                "success": False,
                "message": (
                    "Não é possível excluir a Certificação porque ela está "
                    "relacionada a outros registros."
                )
            })
        except (IntegrityError, DatabaseError) as e:
            return json_error_response(
                message_user="Erro ao excluir a Certificação.",
                exception=e,
                context=f"Exclusão de Certificação {certification.pk}"
            )
        except ValidationError as e:
            return json_error_response(
                message_user="Erro de validação ao excluir a Certificação.",
                exception=e,
                level="warning",
                context=f"Validação ao excluir Certificação {certification.pk}"
            )

    # Renderização do Template
    return render(
        request,
        "certifications/certification_confirmDelete.html",
        {
            "certification": certification,
            "message_confirmation_delete": message_confirmation_delete,
        },
    )
