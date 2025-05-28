# apps/certifications/apps.py

"""
Configuração do app 'certifications' para a aplicação Django.
"""

from django.apps import AppConfig


class CertificationsConfig(AppConfig):
    """Classe de configuração para o aplicativo 'certifications'."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.certifications'
