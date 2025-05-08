# apps/utils/widgets.py

"""
Este módulo contém widgets personalizados para uso em formulários.
"""

from django import forms

class BooleanSelect(forms.Select):
    """
    Um widget de seleção personalizado que representa um campo booleano
    com opções 'Sim' e 'Não'.
    """

    def __init__(self, *args, **kwargs):
        choices = [
            (True, 'Sim'),
            (False, 'Não'),
        ]
        super().__init__(choices=choices, *args, **kwargs)
