# views.py

from django.shortcuts import HttpResponse
from django.core.management import call_command

def migrar_dados(request):
    try:
        call_command('migrate')
        call_command('loaddata', 'dumpdata.json')
        return HttpResponse("Dados migrados com sucesso!")
    except Exception as e:
        return HttpResponse(f"Erro na migração: {e}")
