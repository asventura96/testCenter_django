# apps/clients/views.py

"""
Definição das views para o aplicativo Certifier.
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

from .forms import CertifierForm
from .models import Certifier


def certifier_home(request):
    """View para a Página Inicial de Certificadores."""

    return render(request, "certifiers/certifiers_home.html")


def certifier_list(request):
    """View para Listar os Certificadores."""

    # Obtenção dos Filtros
    query = request.GET.get("certifier-list-query")
    idle = request.GET.get("certifier-list-idle")

    # Ordenação
    order_by = request.GET.get("order_by", "name")
    descending = request.GET.get("descending", "False") == "True"

    # Otimização da Consulta
    certifier = Certifier.objects.all()

    # Filtragem
    if query:
        certifier = certifier.filter(
            Q(name__icontains=query) |
            Q(abbreviation__icontains=query)
        )

    if idle in ["True", "False"]:
        certifier = certifier.filter(idle=(idle == "True"))

    # Aplicação de Filtros da Ordenação
    if descending:
        order_by = f"-{order_by}"
    certifier = certifier.order_by(order_by)

    # Registros por Página
    records_per_page = request.GET.get("records_per_page", 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 10

    # Paginação
    paginator = Paginator(certifier, records_per_page)
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
            "id": "certifier-list-query",
            "name": "certifier-list-query",
            "label": "Busque pelo Nome ou Sigla",
            "placeholder": "Digite o Nome ou Sigla do Certificador",
            "type": "text",
            "value": request.GET.get("q", ""),
        },
        {
            "id": "certifier-list-idle",
            "name": "certifier-list-idle",
            "label": "Certificador Inativo?",
            "type": "select",
            "options": [("True", "Sim"), ("False", "Não")],
            "selected": request.GET.get("idle", ""),
        },
    ]

    context = {
        "certifier": certifier,
        "page_obj": page_obj,
        "search_fields": search_fields,
        "query_params": request.GET.urlencode(),
        "headers": [
            {"field": "id", "label": "ID"},
            {"field": "name", "label": "Nome"},
            {"field": "abbreviation", "label": "Sigla"},
            {"field": "notes", "label": "Observações"},
            {"field": "idle", "label": "Inativo"},
        ],
        "rows": [
            [
                certifier.id,
                mark_safe(
                    f'<a href="{reverse(
                        "certifier_detail",
                        args=[certifier.id]
                    )}">{certifier.name}</a>'
                ),
                certifier.abbreviation,
                certifier.notes,
                "Sim" if certifier.idle else "Não",
            ]
            for certifier in page_obj
        ],
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "includes/table.html", context)
    else:
        return render(request, "certifiers/certifiers_list.html", context)


def certifier_detail(request, pk):
    """View para Visualizar os Detalhes de um Certificador."""

    # Obtenção dos Filtros
    certifier = get_object_or_404(Certifier, pk=pk)

    # Mensagem de confirmação de exclusão do Certificador
    message_confirmation_delete = (
        f'Tem certeza que deseja excluir o Certificador <br>'
        f'<strong>{certifier.name}</strong>?'
    )

    # Preparação dos Dados para o template reutilizável
    tabs = [
        {
            "id": "certifier-detail-dados",
            "class": "btn-detail",
            "label": "Detalhes",
        },
    ]

    sections = [
        {
            "id": "certifier-detail-dados",
            "title": "Detalhes do Certificador",
            "active": True,
            "fields": [
                {
                    "label": "Status do Certificador",
                    "value": "Inativo" if certifier.idle else "Ativo",
                    "label_class": "apps-detail-status-label",
                    "value_class": "apps-detail-status-value",
                },
                {"label": "Sigla", "value": certifier.abbreviation},
                {"label": "Nome do Certificador", "value": certifier.name},
                {
                    "label": "Observações deste Certificador",
                    "value": certifier.notes
                },
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-edit",
            "url": reverse("certifier_edit", args=[certifier.pk]),
            "title": "Editar Certificador",
            "aria-label": "Editar Certificador",
        },
        {
            "class": "btn-delete",
            "url": reverse("certifier_delete", args=[certifier.pk]),
            "data": {
                "model": "Certifier",
                "pk": certifier.pk,
                "redirect-url": reverse("certifier_list"),
            },
            "title": "Excluir Certificador",
            "aria-label": "Excluir Certificador",
        },
        {
            "class": "btn-return",
            "url": reverse("certifier_list"),
            "title": "Voltar para a lista de Certificadores",
            "aria-label": "Voltar para a lista de Certificadores",
        },
    ]

    # Renderização do template
    return render(
        request,
        "certifiers/certifiers_detail.html",
        {
            "certifier": certifier,
            "tabs": tabs,
            "sections": sections,
            "buttons": buttons,
            "message_confirmation_delete": message_confirmation_delete,
        },
    )


def certifier_new(request):
    """View para Adicionar um Certificador."""

    if request.method == "POST":
        form = CertifierForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    "Certificador adicionado com sucesso!"
                )
                return redirect(reverse("certifier_list"))
            except IntegrityError:
                messages.error(
                    request,
                    "Erro: Já existe um Certificador com esta Sigla."
                )
            except DatabaseError as e:
                log_exception(
                    exception=e,
                    context="Erro ao salvar Certificador",
                )
                messages.error(
                    request,
                    "Erro interno ao adicionar o Certificador."
                )
        else:
            messages.error(
                request,
                "Erro ao adicionar o Certificador."
            )
    else:
        form = CertifierForm()

    # Definição das Seções e Botões para o Template
    sections = [
        {
            "title": "Dados do Certificador",
            "fields": [
                form["name"],
                form["abbreviation"],
                form["notes"],
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-return",
            "url": reverse("certifier_list"),
            "title": "Retornar",
            "text": "Retornar",
        },
    ]

    # Renderização do template
    return render(
        request,
        "certifiers/certifiers_form.html",
        {
            "form": form,
            "sections": sections,
            "buttons": buttons,
        },
    )


def certifier_edit(request, pk):
    """View para Editar um Certificador."""

    # Obtenção do objeto pelo ID (pk) ou retorno de erro 404 se não encontrado
    certifier = get_object_or_404(Certifier, pk=pk)

    # Verificação da Requisição do tipo POST
    if request.method == "POST":
        form = CertifierForm(request.POST, instance=certifier)

        # Validação do Formulário
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    "Certificador atualizado com sucesso!"
                )
                return redirect(reverse("certifier_list"))
            except IntegrityError:
                messages.error(
                    request,
                    "Erro: Já existe um Certificador com esta Sigla."
                )
            except DatabaseError as e:
                log_exception(
                    exception=e,
                    context="Erro ao atualizar Certificador",
                )
                messages.error(
                    request,
                    "Erro interno ao atualizar o Certificador."
                )
        else:
            messages.error(
                request,
                "Erro ao atualizar o Certificador."
            )
    else:
        form = CertifierForm(instance=certifier)

    # Definição das Seções e Botões para o Template
    sections = [
        {
            "title": "Dados do Certificador",
            "fields": [
                form["idle"],
                form["name"],
                form["abbreviation"],
                form["notes"],
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-return",
            "url": reverse("certifier_list"),
            "title": "Retornar",
            "text": "Retornar",
        },
    ]

    # Renderização do Template
    return render(
        request,
        "certifiers/certifiers_form.html",
        {
            "form": form,
            "sections": sections,
            "buttons": buttons,
        },
    )


def certifier_delete(request, pk):
    """View para Excluir um Certificador."""

    # Obtenção do objeto pelo ID (pk) ou retorno de erro 404 se não encontrado
    certifier = get_object_or_404(Certifier, pk=pk)

    # Mensagem de confirmação de exclusão do cliente
    message_confirmation_delete = (
        f'Tem certeza que deseja excluir o Certificador <br>'
        f'<strong>{certifier.name}</strong>?'
    )

    # Verificação da Requisição do tipo POST
    if request.method == "POST":
        try:
            certifier.delete()
            messages.success(
                request,
                (
                    f'O Certificador "<strong>{certifier.name}</strong>" '
                    f'foi excluído com sucesso!'
                )
            )
            return JsonResponse({
                "success": True,
                "message": (
                    f'O Cliente "<strong>{certifier.name}</strong>" '
                    f'foi excluído com sucesso!'
                )
            })
        except ProtectedError:
            return JsonResponse({
                "success": False,
                "message": (
                    "Não é possível excluir o Certificador porque ele está "
                    "relacionado a outros registros."
                )
            })
        except (IntegrityError, DatabaseError) as e:
            return json_error_response(
                message_user="Erro ao excluir o Certificador.",
                exception=e,
                context=f"Exclusão de Certificador {certifier.pk}"
            )
        except ValidationError as e:
            return json_error_response(
                message_user="Erro de validação ao excluir o Certificador.",
                exception=e,
                level="warning",
                context=f"Validação ao excluir Certificador {certifier.pk}"
            )

    # Renderização do Template
    return render(
        request,
        "certifiers/certifiers_delete.html",
        {
            "certifier": certifier,
            "message_confirmation_delete": message_confirmation_delete,
        }
    )
