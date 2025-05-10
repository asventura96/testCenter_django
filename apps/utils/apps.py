# apps/utils/utils.py

"""
Configuração do app 'utils' para a aplicação Django.
"""

from django.apps import AppConfig


class UtilsConfig(AppConfig):
    """Classe de configuração para o aplicativo 'utils'."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.utils"
