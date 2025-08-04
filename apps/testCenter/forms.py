# apps/testCenter/forms.py

"""
Definição dos formulários do aplicativo 'testCenter'.
"""

from django import forms

from apps.utils.widgets import BooleanSelect
from apps.certifications.models import Certification
from apps.clients.models import Client

from .models import TestCenter, TestCenterExam


class TestCenterForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Centros de Provas.
    """

    name = forms.CharField(
        label="Nome do Centro de Provas",
        widget=forms.TextInput(
            attrs={
                "class": "apps-form-input",
                "id": "testcenter-name",
                "placeholder": "Digite o Nome do Centro de provas",
                "autofocus": True,
            }
        ),
    )
    idle = forms.BooleanField(
        label="Centro de Provas Inativo",
        required=False,
        widget=BooleanSelect(
            attrs={
                "class": "apps-form-input",
                "id": "testcenter-idle",
            }
        ),
    )
    notes = forms.CharField(
        label="Observações do Centro de Provas",
        widget=forms.Textarea(
            attrs={
                "class": "apps-form-input",
                "id": "testCenter-notes",
                "placeholder": "Digite uma Observação do Centro de Provas",
                "rows": 4,
            }
        ),
        required=False,
    )

    class Meta:
        """Meta-informações para o formulário"""
        model = TestCenter
        fields = [
            "name",
            "idle"
        ]


class TestCenterExamForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Exames
    Realizados no Centro de Provas.
    """

    certification = forms.ModelChoiceField(
        queryset=Certification.objects.all(),
        label="Certificação",
        widget=forms.Select(
            attrs={
                "class": "apps-form-input select2",
                "id": "testCenterExam-certification",
                "placeholder": "Selecione a Certificação",
                "autofocus": True,
            }
        ),
    )
    testCenter = forms.ModelChoiceField(
        queryset=TestCenter.objects.all(),
        label="Centro de Provas",
        widget=forms.Select(
            attrs={
                "class": "apps-form-input select2",
                "id": "testCenterExam-testCenter",
                "placeholder": "Selecione o Centro de Provas",
            }
        ),
    )
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label="Cliente",
        widget=forms.Select(
            attrs={
                "class": "apps-form-input select2",
                "id": "testCenterExam-client",
                "placeholder": "Selecione o Cliente",
            }
        ),
    )
    date = forms.DateTimeField(
        label="Data e Hora do Exame",
        widget=forms.DateTimeInput(
            format="%Y-%m-%d %H:%M",
            attrs={
                "class": "apps-form-input",
                "id": "testCenterExam-date",
                "placeholder": "Selecione a Data e Hora do Exame",
            }
        ),
    )
    presence = forms.BooleanField(
        label="O Cliente compareceu ao Exame?",
        required=False,
        widget=BooleanSelect(
            attrs={
                "class": "apps-form-input",
                "id": "testCenterExam-presence",
            }
        ),
    )
    notes = forms.CharField(
        label="Observações do Exame",
        widget=forms.Textarea(
            attrs={
                "class": "apps-form-input",
                "id": "testCenterExam-notes",
                "placeholder": "Digite uma Observação do Exame",
                "rows": 4,
            }
        ),
        required=False,
    )

    class Meta:
        """Meta-informações para o formulário"""
        model = TestCenterExam
        fields = [
            "certification",
            "testCenter",
            "client",
            "date",
            "presence",
            "notes"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["certification"].queryset = (
            Certification.objects
            .filter(idle=False)
            .order_by("name")
        )
        self.fields["certification"].label_from_instance = (
            self.certification_label_from_instance
        )

        self.fields["client"].queryset = (
            Client.objects
            .filter(idle=False)
            .order_by("name")
        )
        self.fields["client"].label_from_instance = (
            self.client_label_from_instance
        )

    def certification_label_from_instance(self, obj):
        """
        Retorna o rótulo para a Certificação.
        """
        return f"{obj.name} ({obj.examCode})"

    def client_label_from_instance(self, obj):
        """
        Retorna o rótulo para o Cliente.
        """
        return f"{obj.uid}: {obj.name}"
