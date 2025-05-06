# apps/clients/apps.py

"""
Configuração do app 'clients' para a aplicação Django.
"""

from django.apps import AppConfig

class AlunosConfig(AppConfig):
    """ Classe de configuração para o aplicativo 'clients'. """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.clients'
