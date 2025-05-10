# apps/clients/models.py

"""
Definições dos modelos do aplicativo 'clients'.
"""

from django.db import models


class Client(models.Model):
    """Modelo que representa um Cliente no sistema."""

    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    idle = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para definir o UID inicial
        e garantir que o nome seja salvo em caixa alta.

        O UID é gerado automaticamente a partir do último ID utilizado, garantindo a unicidade.
        O nome é convertido para caixa alta para padronizar os dados.
        """

        # Garante que o nome seja salvo em caixa alta
        if self.name:
            self.name = self.name.upper()

        # Lógica para definir o UID inicial
        if self._state.adding and self.uid is None:
            last_id = Client.objects.aggregate(models.Max("uid"))["uid__max"]
            if last_id is None:
                self.uid = 10000000
            else:
                self.uid = last_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        """Retorna uma representação em string do objeto Cliente."""
        return f"Cliente: {self.uid} - {self.name}"

    class Meta:
        """Meta-informações para o modelo Client."""

        db_table = "tb_client"
