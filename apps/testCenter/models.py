# apps/testCenter/models.py

"""
Definições dos modelos do aplicativo 'testCenter'.
"""

from datetime import datetime

from django.db import models

from apps.certifications.models import Certification
from apps.clients.models import Client


class TestCenter(models.Model):
    """Modelo que representa um Centro de Provas no sistema."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    idle = models.BooleanField(default=False)

    def __str__(self):
        """Retorna uma representação em string do objeto TestCenter."""
        return f"Centro de Provas: {self.name}"

    class Meta:
        """Meta-informações para o modelo TestCenter."""
        db_table = "tb_test_center"


class TestCenterExam(models.Model):
    """Modelo que representa um Exame Realizado no Centro de Provas."""

    id = models.AutoField(primary_key=True)
    certification = models.ForeignKey(
        Certification, on_delete=models.PROTECT
    )
    testCenter = models.ForeignKey(TestCenter, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date = models.DateTimeField()
    presence = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        if isinstance(self.date, datetime):
            formatted_date = self.date.strftime("%d/%m/%Y %H:%M")
        else:
            formatted_date = "Data não definida"

        return (
            f"{self.certification.name} - "
            f"{self.testCenter.name} - "
            f"{self.client.name} - "
            f"{formatted_date} - "
        )

    class Meta:
        """Meta-informações para o modelo TestCenterExam."""
        db_table = "tb_testCenter-exam"
