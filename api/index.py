import os
import sys
from django.core.wsgi import get_wsgi_application

# Garante que o Vercel encontre o projeto Django
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "venturix_testCenter.settings")

app = get_wsgi_application()
