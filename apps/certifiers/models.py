# apps/certifiers/models.py

"""
Definições dos modelos do aplicativo 'certifiers'.
"""

from django.db import models


class Certifier(models.Model):
    """Modelo que representa um Certificador no sistema."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=3, unique=True)
    notes = models.TextField(blank=True, null=True)
    idle = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que a abreviação
        seja salva em caixa alta.
        """
        if self.abbreviation:
            self.abbreviation = self.abbreviation.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        """Retorna uma representação em string do objeto Certifier."""
        return f"Certificador: {self.name} ({self.abbreviation})"

    class Meta:
        """Meta-informações para o modelo Certifier."""
        db_table = "tb_certifier"
