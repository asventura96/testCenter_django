# apps/clients/views.py

"""
Definição das views para o aplicativo Client.
"""

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from .forms import ClientForm
from .models import Client


def client_home(request):
    """View para a Página Inicial de Clientes"""
    return render(request, "clients/clients_home.html")


def client_new(request):
    """View para Adicionar um Cliente"""
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("client_list"))
        else:
            print(form.errors)
    else:
        form = ClientForm()

    # Definição das Seções e Botões
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


def client_list(request):
    """View para Listar os Clientes"""
    # Obtém os filtros
    query = request.GET.get("client-list-query")
    idle = request.GET.get("client-list-idle")

    # Ordenação
    order_by = request.GET.get("order_by", "name")
    descending = request.GET.get("descending", "False") == "True"

    # Otimização da Consulta
    client = Client.objects.all()

    # Filtragem
    if query:
        client = client.filter(Q(id__icontains=query) | Q(name__icontains=query))

    if idle in ["True", "False"]:
        client = client.filter(idle=idle == "True")

    # Aplicação da Ordenação
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

    # Tratamento de erros para garantir que o objeto de página seja válido
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
            "placeholder": "Busque pelo Nome ou UID do Cliente",
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
            {"field": "id", "label": "ID"},
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
    """View para Visualizar os detalhes de um Cliente"""
    # Obtenção dos filtros
    client = get_object_or_404(Client, pk=pk)

    # Preparação dos Dados para o template reutilizável
    tabs = [
        {"id": "client-detail-dados", "class": "btn-detail", "label": "Detalhes"},
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
            "data": {"model": "Client", "pk": client.pk},
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
        },
    )


def client_edit(request, pk):
    """View para Editar um Cliente"""
    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    client = get_object_or_404(Client, pk=pk)

    # Verifica se a requisição é do tipo POST (submissão de formulário)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)

        # Se o formulário for válido, salva as alterações no objeto
        if form.is_valid():
            form.save()
            return redirect("client_list")
    else:
        form = ClientForm(instance=client)

    # Definição das Seções e Botões
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


def client_delete(request, pk):
    """View para Excluir um Cliente"""
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.delete()
        return redirect("client_list")
    return render(request, "clients/clients_confirmDelete.html", {"client": client})
