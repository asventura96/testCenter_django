"""
Módulo de views utilitárias para o projeto.

Inclui views para tarefas administrativas, como migrações de dados.
ATENÇÃO: Estas views podem expor funcionalidades sensíveis e devem
ser protegidas por autenticação (ex: @staff_member_required) em produção.
"""
import logging
from django.shortcuts import HttpResponse
from django.core.management import call_command
from django.core.management.base import CommandError
# Para proteger a view em produção, descomente a linha abaixo:
# from django.contrib.admin.views.decorators import staff_member_required

# Configura o logger
logger = logging.getLogger(__name__)


# Para proteger a view, descomente o decorador abaixo:
# @staff_member_required
def migrar_dados(request):
    """
    View administrativa para executar 'migrate' e 'loaddata dumpdata.json'.

    Esta view é uma conveniência de desenvolvimento e NÃO DEVE ser exposta
    publicamente em produção sem a devida autenticação
    (ex: @staff_member_required).
    """
    try:
        call_command('migrate')
        call_command('loaddata', 'dumpdata.json')
        return HttpResponse("Dados migrados com sucesso!")

    except CommandError as e:
        # Erro esperado (ex: 'dumpdata.json' não encontrado)
        # Loga o erro real (usando a formatação lazy que o Pylint prefere)
        logger.error("Erro de comando na migração: %s", e)
        # Retorna uma mensagem genérica para o usuário
        return HttpResponse(
            "Erro ao executar o comando de migração.", status=500
        )

    # Desabilitamos o alerta W0718 pois queremos intencionalmente
    # capturar qualquer outra exceção como um último recurso.
    # pylint: disable=broad-exception-caught
    except Exception as e:
        # Erro inesperado (ex: banco de dados offline)
        # Loga o erro real (usando a formatação lazy)
        logger.error("Erro inesperado na migração: %s", e)
        # Retorna uma mensagem genérica para o usuário
        return HttpResponse("Ocorreu um erro interno inesperado.", status=500)
