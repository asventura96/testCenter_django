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
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'client-name',
                'name': 'client-name',
                'label': 'Nome do Cliente: ',
                'placeholder': 'Digite o Nome do Cliente',
                'autofocus': True,
            }),
            'country': forms.TextInput(attrs={
                'class': 'apps-form-input logradouro-input',
                'id': 'client-country',
                'name': 'client-country',
                'label': 'País: ',
                'placeholder': 'Informe o País do Cliente',
            }),
            'city': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'client-city',
                'name': 'client-city',
                'label': 'Cidade / Estado: ',
                'placeholder': 'Informe a Cidade / Estado do Cliente',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'apps-form-input',
                'id': 'client-notes',
                'name': 'client-notes',
                'label': 'Observações deste Cliente: ',
                'placeholder': 'Digite uma Observação deste Cliente',
                'rows': 4,
            }),
        }
