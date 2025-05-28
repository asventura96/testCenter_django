# apps/clients/views.py

"""
Definição das views para o aplicativo Client.
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

from .forms import ClientForm
from .models import Client


def client_home(request):
    """View para a Página Inicial de Clientes"""

    return render(request, "clients/clients_home.html")


def client_list(request):
    """View para Listar os Clientes"""

    # Obtenção dos Filtros
    query = request.GET.get("client-list-query")
    idle = request.GET.get("client-list-idle")

    # Ordenação
    order_by = request.GET.get("order_by", "name")
    descending = request.GET.get("descending", "False") == "True"

    # Otimização da Consulta
    client = Client.objects.all()

    # Filtragem
    if query:
        client = client.filter(
            Q(uid__icontains=query) |
            Q(name__icontains=query)
        )

    if idle in ["True", "False"]:
        client = client.filter(idle=idle == "True")

    # Aplicação de Filtros da Ordenação
    if descending:
        order_by = f"-{order_by}"
    client = client.order_by(order_by)

    # Registros por Página
    records_per_page = request.GET.get("records_per_page", 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 10

    # Paginação
    paginator = Paginator(client, records_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Tratamento de Erros na Páginação
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Definição dos Campos de Pesquisa
    search_fields = [
        {
            "id": "client-list-query",
            "name": "client-list-query",
            "label": "Busque pelo Nome ou UID do Cliente:",
            "placeholder": "Digite o Nome ou UID do Cliente",
            "type": "text",
            "value": request.GET.get("q", ""),
        },
        {
            "id": "client-list-idle",
            "name": "client-list-idle",
            "label": "Cliente Inativo?",
            "type": "select",
            "options": [("True", "Sim"), ("False", "Não")],
            "selected": request.GET.get("idle", ""),
        },
    ]

    context = {
        "client": client,
        "page_obj": page_obj,
        "search_fields": search_fields,
        "query_params": request.GET.urlencode(),
        "headers": [
            {"field": "uid", "label": "ID"},
            {"field": "nome", "label": "Nome"},
            {"field": "country", "label": "País"},
            {"field": "city", "label": "Cidade"},
            {"field": "notes", "label": "Observações"},
            {"field": "inativo", "label": "Inativo"},
        ],
        "rows": [
            [
                client.uid,
                mark_safe(
                    f'<a href="{reverse(
                        "client_detail",
                        args=[client.uid]
                    )}">{client.name}</a>'
                ),
                client.country,
                client.city,
                client.notes,
                "Sim" if client.idle else "Não",
            ]
            for client in page_obj
        ],
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "includes/table.html", context)
    else:
        return render(request, "clients/clients_list.html", context)


def client_detail(request, pk):
    """View para Visualizar os Detalhes de um Cliente"""

    # Obtenção dos filtros
    client = get_object_or_404(Client, pk=pk)

    # Mensagem de confirmação de exclusão do Cliente
    message_confirmation_delete = (
        f'Tem certeza que deseja excluir o Cliente <br>'
        f'<strong>{client.name}</strong>?'
    )

    # Preparação dos Dados para o template reutilizável
    tabs = [
        {
            "id": "client-detail-dados",
            "class": "btn-detail",
            "label": "Detalhes"
        },
    ]

    sections = [
        {
            "id": "client-detail-dados",
            "title": "Detalhes do Cliente",
            "active": True,
            "fields": [
                {
                    "label": "Status do Cliente",
                    "value": "Inativo" if client.idle else "Ativo",
                    "label_class": "apps-detail-status-label",
                    "value_class": "apps-detail-status-value",
                },
                {"label": "UID", "value": client.uid},
                {"label": "Nome do Cliente", "value": client.name},
                {"label": "País", "value": client.country},
                {"label": "Cidade / Estado", "value": client.city},
                {"label": "Observações deste Cliente", "value": client.notes},
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-edit",
            "url": reverse("client_edit", args=[client.pk]),
            "title": "Editar Cliente",
            "aria-label": "Editar Cliente",
        },
        {
            "class": "btn-delete",
            "url": reverse("client_delete", args=[client.pk]),
            "data": {
                "model": "Client",
                "pk": client.pk,
                "redirect-url": reverse("client_list"),
            },
            "title": "Excluir Cliente",
            "aria-label": "Excluir Cliente",
        },
        {
            "class": "btn-return",
            "url": reverse("client_list"),
            "title": "Voltar para a lista de Clientes",
            "aria-label": "Voltar para a lista de Clientes",
        },
    ]

    # Renderização do template
    return render(
        request,
        "clients/clients_detail.html",
        {
            "client": client,
            "tabs": tabs,
            "sections": sections,
            "buttons": buttons,
            "message_confirmation_delete": message_confirmation_delete,
        },
    )


def client_new(request):
    """View para Adicionar um Cliente"""

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    "Cliente adicionado com sucesso!"
                )
                return redirect(reverse("client_list"))
            except IntegrityError:
                messages.error(
                    request,
                    "Erro: já existe um Cliente com este UID."
                )
            except DatabaseError as e:
                log_exception(
                    exception=e,
                    context="Erro ao salvar cliente",
                )
                messages.error(
                    request,
                    "Erro interno ao adicionar o Cliente."
                )
        else:
            messages.error(
                request,
                "Erro ao adicionar o Cliente."
            )
    else:
        form = ClientForm()

    # Definição das Seções e Botões para o Template
    sections = [
        {
            "title": "Dados do Cliente",
            "fields": [
                form["name"],
                form["country"],
                form["city"],
                form["notes"],
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-return",
            "url": reverse("client_list"),
            "title": "Retornar",
            "text": "Retornar",
        },
    ]

    # Renderização do template
    return render(
        request,
        "clients/clients_form.html",
        {
            "form": form,
            "sections": sections,
            "buttons": buttons,
        },
    )


def client_edit(request, pk):
    """View para Editar um Cliente"""

    # Obtenção do objeto pelo ID (pk) ou retorno de erro 404 se não encontrado
    client = get_object_or_404(Client, pk=pk)

    # Verificação da Requisição do tipo POST
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)

        # Validação do Formulário
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    "Cliente atualizado com sucesso!"
                )
                return redirect(reverse("client_list"))
            except IntegrityError:
                messages.error(
                    request,
                    "Erro: já existe um Cliente com este UID."
                )
            except DatabaseError as e:
                log_exception(
                    exception=e,
                    context="Erro ao atualizar Cliente",
                )
                messages.error(
                    request,
                    "Erro interno ao atualizar o Cliente."
                )
        else:
            messages.error(
                request,
                "Erro ao atualizar o Cliente."
            )
    else:
        form = ClientForm(instance=client)

    # Definição das Seções e Botões para o Template
    sections = [
        {
            "title": "Dados do Cliente",
            "fields": [
                form["idle"],
                form["name"],
                form["country"],
                form["city"],
                form["notes"],
            ],
        },
    ]

    buttons = [
        {
            "class": "btn-return",
            "url": reverse("client_list"),
            "title": "Retornar",
            "text": "Retornar",
        },
    ]

    # Renderização do Template
    return render(
        request,
        "clients/clients_form.html",
        {
            "form": form,
            "sections": sections,
            "buttons": buttons,
        },
    )


def client_delete(request, pk):
    """View para Excluir um Cliente"""

    # Obtenção do objeto pelo ID (pk) ou retorno de erro 404 se não encontrado
    client = get_object_or_404(Client, pk=pk)

    # Mensagem de confirmação de exclusão do cliente
    message_confirmation_delete = (
        f'Tem certeza que deseja excluir o Cliente <br>'
        f'<strong>{client.name}</strong>?'
    )

    # Verificação da Requisição do tipo POST
    if request.method == "POST":
        try:
            client.delete()
            messages.success(
                request,
                (
                    f'O Cliente "<strong>{client.name}</strong>" '
                    f'foi excluído com sucesso!'
                )
            )
            return JsonResponse({
                "success": True,
                "message": (
                    f'O Cliente "<strong>{client.name}</strong>" '
                    f'foi excluído com sucesso!'
                )
            })
        except ProtectedError:
            return JsonResponse({
                "success": False,
                "message": (
                    "Não é possível excluir o Cliente porque ele está "
                    "relacionado a outros registros."
                )
            })
        except (IntegrityError, DatabaseError) as e:
            return json_error_response(
                message_user="Erro ao excluir o Cliente.",
                exception=e,
                context=f"Exclusão de Cliente {client.pk}"
            )
        except ValidationError as e:
            return json_error_response(
                message_user="Erro de validação ao excluir o Cliente.",
                exception=e,
                level="warning",
                context=f"Validação ao excluir Cliente {client.pk}"
            )

    # Renderização do Template
    return render(
        request,
        "clients/clients_confirmDelete.html",
        {
            "client": client,
            "message_confirmation_delete": message_confirmation_delete,
        }
    )
