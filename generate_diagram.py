# generate_diagram.py

"""
Este script gera um diagrama de modelos do Django em formato PDF.
Ele utiliza a biblioteca Tkinter para permitir que o usuário selecione
um diretório onde o diagrama será salvo. O script executa o comando
`graph_models` do Django para gerar o diagrama com base nas aplicações
instaladas no projeto.
"""

import os
import sys
import subprocess
import tkinter as tk

from tkinter import filedialog
from datetime import datetime

import django

from django.conf import settings


# Define o DJANGO_SETTINGS_MODULE antes de chamar django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testCenter.settings")
django.setup()


def get_project_apps():
    """
    Retorna uma lista de nomes de aplicativos instalados no projeto Django,
    excluindo aqueles que pertencem ao Django e ao allauth.
    A lista é composta apenas pelos nomes dos aplicativos, sem o prefixo do
    módulo.
    """

    return [
        app.split('.')[-1]
        for app in settings.INSTALLED_APPS
        if not app.startswith("django.") and not app.startswith("allauth")
    ]


apps = get_project_apps()


def generate_diagram():
    """
    Gera um diagrama de modelos e solicita ao usuário um diretório
    para salvar o arquivo PDF resultante.
    """

    # Cria uma instância da janela Tkinter
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    # Abre o pop-up de seleção de pasta para salvar o diagrama
    save_directory = filedialog.askdirectory(
        title="Selecione a pasta para salvar o diagrama"
    )

    # Verifica se o usuário selecionou uma pasta
    if save_directory:
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Obtém a data e hora atual
        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M")

        # Define o nome do arquivo com a data e hora atual
        file_name = f"testCenter_diagram_{date_time}.pdf"
        file_path = os.path.join(save_directory, file_name)

        # Define o caminho para o manage.py
        manage_py_path = os.path.join(os.getcwd(), 'manage.py')

        # Verifica se o arquivo manage.py existe
        if os.path.exists(manage_py_path):
            # Gera o diagrama em formato PDF
            result = subprocess.run(
                [sys.executable, manage_py_path, "graph_models", *apps,
                 "--group-models", "-o", file_path],
                capture_output=True, text=True)

            # Verifica se houve algum erro durante a execução do comando
            if result.returncode != 0:
                print("Erro ao gerar o diagrama:")
                print(result.stderr)
            else:
                print(f"Diagrama gerado com sucesso: {file_path}")
        else:
            print(
                f"O arquivo manage.py não foi encontrado no diretório atual: "
                f"{os.getcwd()}"
            )
    else:
        print("Nenhuma pasta selecionada para salvar o diagrama.")


if __name__ == "__main__":
    generate_diagram()
