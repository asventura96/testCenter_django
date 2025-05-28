# apps/clients/forms.py

"""
Definição dos formulários do aplicativo 'clients'.
"""

from django import forms

from apps.utils.widgets import BooleanSelect

from .models import Client


class ClientForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Clientes.
    """

    name = forms.CharField(
        label="Nome do Cliente",
        widget=forms.TextInput(
            attrs={
                "class": "apps-form-input",
                "id": "client-name",
                "placeholder": "Digite o Nome do Cliente",
                "autofocus": True,
            }
        ),
    )
    country = forms.CharField(
        label="País",
        widget=forms.TextInput(
            attrs={
                "class": "apps-form-input logradouro-input",
                "id": "client-country",
                "placeholder": "Informe o País do Cliente",
            }
        ),
    )
    city = forms.CharField(
        label="Cidade / Estado",
        widget=forms.TextInput(
            attrs={
                "class": "apps-form-input",
                "id": "client-city",
                "placeholder": "Informe a Cidade / Estado do Cliente",
            }
        ),
    )
    notes = forms.CharField(
        label="Observações deste Cliente",
        widget=forms.Textarea(
            attrs={
                "class": "apps-form-input",
                "id": "client-notes",
                "placeholder": "Digite uma Observação deste Cliente",
                "rows": 4,
            }
        ),
        required=False,
    )
    idle = forms.BooleanField(
        label="Cliente Inativo",
        required=False,
        widget=BooleanSelect(
            attrs={
                "class": "apps-form-input",
                "id": "client-idle",
            }
        ),
    )

    class Meta:
        """Meta-informações para o formulário."""

        model = Client
        fields = ["name", "country", "city", "notes", "idle"]
