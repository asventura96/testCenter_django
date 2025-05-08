# testCenter/settings.py

"""
Configurações do Django para o projeto Test Center.

Este módulo contém as configurações para o projeto Django siga, incluindo
configurações para o banco de dados, aplicativos instalados, middlewares e muito mais.
"""

import os
import environ

# Definição do diretório base do projeto (BASE_DIR)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Inicializa o django-environ
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Configuração da chave secreta (SECRET_KEY)
SECRET_KEY = env('SECRET_KEY')

# Configuração do modo de depuração (DEBUG) baseado na variável de ambiente
DEBUG = env.bool('DEBUG', default=False)

# Configuração dos hosts permitidos (ALLOWED_HOSTS) para produção
ALLOWED_HOSTS = env(
    'ALLOWED_HOSTS',
    default='127.0.0.1,localhost' if DEBUG else '127.0.0.1,localhost'
).split(',')

# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, env('SQLITE_PATH', default='data/db.sqlite3')),
    }
}

# Configuração de cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',  # Endereço do servidor Memcached
    }
}

# Configuração de cache em memória para ambiente de desenvolvimento
if DEBUG:
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',  # Identificador único para o cache em memória
    }

# Configuração de sessão
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'  # O alias do cache definido anteriormente

# Configuração dos aplicativos instalados (INSTALLED_APPS)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_bootstrap5',
    'testCenter',
    'apps.clients',  # Aplicativo de Clientes
]

# Configuração dos middlewares (MIDDLEWARE)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'testCenter.middleware.LoginRequiredMiddleware',
]

# Configuração dos templates (TEMPLATES)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração da URL principal (ROOT_URLCONF)
ROOT_URLCONF = 'testCenter.urls'

# Configuração da aplicação WSGI (WSGI_APPLICATION)
WSGI_APPLICATION = 'testCenter.wsgi.application'

# Configuração de validação de senhas (AUTH_PASSWORD_VALIDATORS)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuração de login/logout
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# Configurações de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_errors.log'),
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Internacionalização e localização (I18N, L10N, TIME_ZONE)
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Configuração de arquivos estáticos (STATIC_URL, STATICFILES_DIRS)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configurações de Segurança
SESSION_COOKIE_SECURE = True  # Envia o cookie de sessão apenas por HTTPS
SESSION_COOKIE_HTTPONLY = True  # Impede que o cookie seja acessado via JavaScript
SESSION_COOKIE_SAMESITE = 'Lax'  # Reduz o risco de vazamento de cookies em requisições cross-site

# Configuração do STATIC_ROOT para produção
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuração do CSP (Content Security Policy)
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': (
            "'self'",
        ),
        'img-src': (
            "'self'",
            'data:',
        ),
        'script-src': (
            "'self'",
            "'unsafe-inline'",
            'https://cdn.jsdelivr.net'
        ),
        'style-src': (
            "'self'",
            "'unsafe-inline'",
            'https://cdn.jsdelivr.net'
        )
    }
}
