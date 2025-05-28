# apps/certifiers/forms.py

"""
Definição dos formulários do aplicativo 'certifiers'.
"""

from django import forms

from apps.utils.widgets import BooleanSelect

from .models import Certifier


class CertifierForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Certificadores.
    """

    name = forms.CharField(
        label="Nome do Certificador",
        widget=forms.TextInput(
            attrs={
                "class": "apps-form-input",
                "id": "certifier-name",
                "placeholder": "Digite o Nome do Certificador",
                "autofocus": True,
            }
        ),
    )
    abbreviation = forms.CharField(
        label="Sigla do Certificador",
        widget=forms.TextInput(
            attrs={
                "class": "apps-form-input",
                "id": "certifier-abbreviation",
                "placeholder": "Informe a Sigla do Certificador",
            }
        ),
    )
    notes = forms.CharField(
        label="Observações deste Certificador",
        widget=forms.Textarea(
            attrs={
                "class": "apps-form-input",
                "id": "certifier-notes",
                "placeholder": "Digite uma Observação deste Certificador",
                "rows": 4,
            }
        ),
        required=False,
    )
    idle = forms.BooleanField(
        label="Certificador Inativo",
        required=False,
        widget=BooleanSelect(
            attrs={
                "class": "apps-form-input",
                "id": "certifier-idle",
            }
        ),
    )

    class Meta:
        """Meta-informações para o formulário."""
        model = Certifier
        fields = ["name", "abbreviation", "notes", "idle"]
