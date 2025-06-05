# apps/testCenter/apps.py

"""
Configuração do app 'testCenter' para a aplicação Django.
"""

from django.apps import AppConfig


class TestCenterConfig(AppConfig):
    """Classe de configuração para o aplicativo 'testCenter'."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.testCenter"
