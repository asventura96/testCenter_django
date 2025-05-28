# testCenter/views.py

"""
Este módulo define as views da aplicação, incluindo funções para exclusão de
itens e exibição da página inicial. A função `delete_item` exclui um item
específico de um modelo identificado pelo nome e PK, enquanto `home` renderiza
a página inicial do projeto.
"""

from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt


# ----- View para a Página Inicial do Projeto -----
def home(request):
    """
    Renderiza a página inicial do projeto.

    Parâmetros:
    - request: Objeto HttpRequest representando a requisição HTTP recebida.

    Retorna:
    - HttpResponse: Resposta HTTP que renderiza o template da página inicial.
    """
    return render(request, "home.html")


@csrf_exempt  # Use com cautela
def delete_item(request, model_name, pk):
    """
    Exclui um item de um modelo específico baseado no nome do modelo
    e na chave primária (PK).

    Parâmetros:
    - request: Objeto HttpRequest representando a requisição HTTP recebida.
    - model_name (str): Nome do modelo do qual o item será excluído.
    - pk (int): Chave primária do item a ser excluído.

    Retorna:
    - JsonResponse: Resposta JSON indicando sucesso ou falha na operação.
    """
    print(
        f"Requisição recebida: {request.method}, "
        f"Modelo: {model_name}, PK: {pk}"
    )
    if request.method == "POST":
        try:
            model = None
            for app in apps.get_app_configs():
                try:
                    model = app.get_model(model_name)
                    break
                except LookupError:
                    continue
            if not model:
                print("Modelo não encontrado.")  # Modelo não encontrado
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Modelo não encontrado"
                    },
                    status=404
                )

            # Obter o item e excluir
            item = get_object_or_404(model, pk=pk)
            item.delete()
            print(f"Item excluído: {item}")  # Adicione este print

            # Retornar uma resposta de sucesso sem redirecionar
            return JsonResponse({"success": True})
        except ImportError as e:
            print(f"Erro ao excluir o item: {e}")
            return JsonResponse(
                {
                    "success": False,
                    "error": "Ocorreu um erro interno ao excluir o item.",
                },
                status=500,
            )
    print("Método não permitido.")
    return JsonResponse(
        {
            "success": False,
            "error": "Método não permitido"
        },
        status=405
    )
