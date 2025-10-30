# testCenter_django

Este repositório contém o projeto Django **testCenter_django**. O objetivo do projeto
é o gerenciamento de exames e provas no contexto de um Centro de Provas,
incluindo funcionalidades de backend e integração para aplicações web.

Este guia é focado na instalação e configuração do ambiente de desenvolvimento.

## Índice 🗺️

1. [Pré-requisitos](#pré-requisitos-)
2. [Instalação (Desenvolvimento)](#instalação-desenvolvimento-)
3. [Configuração](#configuração-)
4. [Executando o Projeto](#executando-o-projeto-)
5. [Estrutura do Projeto](#estrutura-do-projeto-)
6. [Contribuição](#contribuição-)
7. [Licença](#licença-)

## Pré-requisitos ✅

Certifique-se de ter as seguintes ferramentas instaladas:

- [Python](https://www.python.org/) (Versão `>=3.10,<4.0`, conforme `pyproject.toml`)
- [Poetry](https://python-poetry.org/) (Gerenciador de dependências)
- Banco de dados compatível com Django (ex.: PostgreSQL, MySQL, SQLite)

## Instalação (Desenvolvimento) 🔧

1. Clone o repositório:

```bash
git clone https://github.com/asventura96/testCenter_django.git
cd testCenter_django
```

2. Instale as dependências usando o Poetry:

```bash
poetry install
```

   *(Este comando irá criar automaticamente um ambiente virtual
   e instalar todas as dependências do `poetry.lock`)*.

3. Ative o ambiente virtual criado pelo Poetry:

```bash
poetry shell
```

   *(A partir de agora, todos os comandos `python` ou `django-admin`
   serão executados dentro deste ambiente)*.

## Configuração ⚙️

1. **Variáveis de Ambiente:**
Este projeto usa um arquivo `.env` para gerenciar variáveis de ambiente
(como chaves de API e configurações de banco de dados).

Copie o arquivo de exemplo (você pode precisar criar o `.env.example` primeiro)
para o seu arquivo local:

```bash
cp .env.example .env
```

Em seguida, edite o arquivo `.env` e preencha as variáveis necessárias, como:

```text
SECRET_KEY='sua_chave_secreta_aqui'
DEBUG=True
DATABASE_URL='sqlite:///db.sqlite3'
# ... outras variáveis (ex: Email, S3, etc.)
```

2. **Migrações do Banco de Dados:**
Com o ambiente ativo (`poetry shell`), execute as migrações:

```bash
python manage.py migrate
```

3. **(Opcional) Crie um Superusuário:**

```bash
python manage.py createsuperuser
```

## Executando o Projeto 🚀

1. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

2. Acesse o projeto no seu navegador:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Estrutura do Projeto 📦

A estrutura segue as boas práticas de um projeto Django, separando a
configuração (`venturix_testCenter`) dos aplicativos (`apps`).

```text
testCenter_django/
├── .testCenterVenv/      # Ambiente virtual (gerenciado pelo Poetry)
├── venturix_testCenter/  # Pasta do PROJETO (contém settings.py)
│   ├── settings.py
│   └── urls.py
├── apps/                 # Pasta contendo todos os APPs do projeto
│   ├── api/
│   │   ├── models.py
│   │   ├── views.py
│   │   └── ...
│   ├── (outros_apps_aqui)/
│   └── ...
├── static/               # Arquivos estáticos globais
├── templates/            # Templates HTML globais
├── manage.py             # Script de gerenciamento do Django
├── pyproject.toml        # Arquivo de configuração do Poetry
├── poetry.lock           # Lockfile do Poetry
├── requirements.txt      # Exportado do Poetry (para deploy/CI)
└── README.md
```

## Contribuição 🤝

Contribuições são bem-vindas! Siga as etapas abaixo:

1. Faça um fork deste repositório.
2. Crie um branch para sua feature: `git checkout -b minha-feature`
3. Faça o commit de suas alterações: `git commit -m "Minha nova feature"`
4. Faça o push para o branch: `git push origin minha-feature`
5. Abra um pull request.

## Licença ⚖️

Este projeto é licenciado sob os termos da **Licença GPL-3.0**.

Veja o arquivo `LICENSE` no repositório para mais detalhes.

---

**Contato do Autor:** [asventura96](https://github.com/asventura96)
