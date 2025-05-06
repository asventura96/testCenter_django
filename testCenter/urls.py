# testCenter/urls.py

"""
URLs do projeto siga.

Este módulo configura as URLs para o projeto siga, incluindo as URLs do aplicativo alunos
e as URLs para login e logout.
"""

from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # URL para a interface Administrativa Django
    path('admin/', admin.site.urls),

    # URL para a Página Inicial do Projeto
    path('', home, name='home'),

    # URLs de Login e Logout do Usuário
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
