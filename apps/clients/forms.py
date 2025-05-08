# apps/clients/forms.py

"""
Este módulo contém os formulários utilizados para o aplicativo de Alunos.
Ele define os formulários para cadastro, edição e outras operações relacionadas aos Alunos.
"""

from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Clientes.
    """
    name = forms.CharField(
        label='Nome do Cliente',
        widget=forms.TextInput(attrs={
            'class': 'apps-form-input',
            'id': 'client-name',
            'placeholder': 'Digite o Nome do Cliente',
            'autofocus': True,
        })
    )
    country = forms.CharField(
        label='País',
        widget=forms.TextInput(attrs={
            'class': 'apps-form-input logradouro-input',
            'id': 'client-country',
            'placeholder': 'Informe o País do Cliente',
        })
    )
    city = forms.CharField(
        label='Cidade / Estado',
        widget=forms.TextInput(attrs={
            'class': 'apps-form-input',
            'id': 'client-city',
            'placeholder': 'Informe a Cidade / Estado do Cliente',
        })
    )
    notes = forms.CharField(
        label='Observações deste Cliente',
        widget=forms.Textarea(attrs={
            'class': 'apps-form-input',
            'id': 'client-notes',
            'placeholder': 'Digite uma Observação deste Cliente',
            'rows': 4,
        }),
        required=False
    )

    class Meta:
        """ Configurações meta do formulário."""
        model = Client
        fields = [
            'name',
            'country',
            'city',
            'notes',
            'idle'
        ]
