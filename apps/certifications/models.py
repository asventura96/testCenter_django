# apps/certifications/models.py

"""
Definições dos modelos do aplicativo 'certifications'.
"""

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.certifiers.models import Certifier


class Certification(models.Model):
    """Modelo que representa uma Certificação no sistema."""

    id = models.CharField(max_length=7, primary_key=True)
    certifier = models.ForeignKey(Certifier, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    examCode = models.CharField(max_length=50, blank=True, null=True)
    durantion = models.PositiveIntegerField(default=0, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    idle = models.BooleanField(default=False)

    def __str__(self):
        """Retorna uma representação em string do objeto Certification."""
        return f"Certificação: {self.name} ({self.examCode})"

    class Meta:
        """Meta-informações para o modelo Certification."""
        db_table = "tb_certification"


@receiver(pre_save, sender=Certification)
def set_certification_id(sender, instance, **kwargs):

    # Lógica para definir o ID da certificação
    if not instance.id:
        # Geração de um ID único baseado na Sigla do Certificador
        examCode = instance.certifier.abbreviation

        # Obtenção do último ID usado para a certificação com o mesmo examCode
        last_certification = (
            Certification.objects.
            filter(id__startwith=examCode)
            .order_by('-id')
            .first()
        )

        if last_certification:
            # Incrementação do Número Sequencial
            last_number = int(last_certification.id[-4:])
            new_number = last_number + 1
        else:
            # Se não houver certificações anteriores, inicia com 1
            new_number = 1

        # Formatação do novo ID com o padrão "ABC0001"
        instance.id = f"{examCode}{new_number:04d}"
