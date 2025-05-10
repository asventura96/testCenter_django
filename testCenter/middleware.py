# testCenter/middleware.py

"""
Middleware para garantir que o usuário esteja autenticado antes de acessar certas URLs.
"""

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy

EXEMPT_URLS = [
    settings.LOGIN_URL.lstrip("/"),
    "recuperar-senha/",
    "recuperar-senha/sucesso/",
    "reset/",
    "reset/sucesso/",
    reverse_lazy("login"),
    reverse_lazy("logout"),
]


class LoginRequiredMiddleware:
    """
    Middleware que redireciona usuários não autenticados para a página de login.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip("/")
        if not request.user.is_authenticated:
            if not any(path.startswith(str(url)) for url in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)
