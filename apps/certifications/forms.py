# apps/certifications/forms.py

"""
Definição dos formulários do aplicativo 'certifications'.
"""

from django import forms

from apps.utils.widgets import BooleanSelect
from apps.certifications.models import Certifier

from .models import Certification


class CertificationForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Certificações.
    """

    certifier = forms.ModelChoiceField(
        queryset=Certifier.objects.all(),
        label="Certificador",
        widget=forms.Select(
            attrs={
                "class": "apps-form-input select2",
                "id": "certification-certifier",
                "placeholder": "Selecione o Certificador",
                "autofocus": True,
            }
        ),
    )
    name = forms.CharField(
        label="Nome da Certificação",
        widget=forms.TextInput(
            attrs={
                "class": "apps-form-input",
                "id": "certification-name",
                "placeholder": "Digite o Nome da Certificação",
            }
        ),
    )
    examCode = forms.CharField(
        label="Código do Exame",
        widget=forms.TextInput(
            attrs={
                "class": "apps-form-input",
                "id": "certification-examCode",
                "placeholder": "Informe o Código do Exame",
            }
        ),
    )
    duration = forms.IntegerField(
        label="Duração (em minutos)",
        widget=forms.NumberInput(
            attrs={
                "class": "apps-form-input",
                "id": "certification-duration",
                "placeholder": "Informe a Duração em minutos",
            }
        ),
        min_value=0,
    )
    notes = forms.CharField(
        label="Observações desta Certificação",
        widget=forms.Textarea(
            attrs={
                "class": "apps-form-input",
                "id": "certification-notes",
                "placeholder": "Digite uma Observação desta Certificação",
                "rows": 4,
            }
        ),
        required=False,
    )
    idle = forms.BooleanField(
        label="Certificação Inativa",
        required=False,
        widget=BooleanSelect(
            attrs={
                "class": "apps-form-input",
                "id": "certification-idle",
            }
        ),
    )

    class Meta:
        """Meta-informações para o formulário."""
        model = Certification
        fields = [
            "certifier",
            "name",
            "examCode",
            "duration",
            "notes",
            "idle"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["certifier"].queryset = (
            Certifier.objects
            .filter(idle=False)
            .order_by("name")
        )

        self.fields["certifier"].label_from_instance = (
            self.certifier_label_from_instance
        )

    def certifier_label_from_instance(self, obj):
        """
        Retorna o rótulo para o Certificador.
        """
        return f"{obj.name} ({obj.abbreviation})"
