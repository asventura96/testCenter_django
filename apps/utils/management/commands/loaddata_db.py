# meuapp/management/commands/loaddata_db.py
from django.core.management import BaseCommand, call_command

class Command(BaseCommand):
    help = 'Cria as tabelas do banco de dados e carrega o dump de dados iniciais.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando migrações e carregamento de dados...'))
        
        # Cria a estrutura das tabelas
        call_command('migrate')
        
        # Carrega os dados do dumpdata.json
        call_command('loaddata', 'dumpdata.json')
        
        self.stdout.write(self.style.SUCCESS('Migrações e carregamento concluídos com sucesso!'))