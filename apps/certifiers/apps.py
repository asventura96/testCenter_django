# apps/certifiers/apps.py

"""
Configuração do app 'certifiers' para a aplicação Django.
"""

from django.apps import AppConfig


class CertifiersConfig(AppConfig):
    """Classe de configuração para o aplicativo 'certifiers'."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.certifiers'
