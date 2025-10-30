# 📦 Gerenciamento de Dependências com Poetry e Exportação para requirements.txt

Este guia documenta o processo de uso do Poetry com Python moderno (3.10+)
e a exportação correta para `requirements.txt`.

---

## ✅ Pré-requisitos

- Python **3.10** até **3.15**
(o seu `pyproject.toml` atual `requires-python = ">=3.10,<4.0"` já cobre isso)
- Poetry **versão 1.2+** (recomendado: `1.7+` ou `2.2+`)
- Ambiente virtual ativo (`.venv`)

---

## 🔧 1. Criar ambiente virtual com Python compatível

(Opcional, mas recomendado, se você não tiver um `.venv`)

### Windows (PowerShell)

Isso usará a versão `python` principal do seu PATH (no seu caso, 3.14).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 📦 2. Instalar ou atualizar o Poetry

### Se foi instalado com pip

```bash
pip install --upgrade poetry
```

### Se foi instalado com o instalador oficial

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

---

## 🧩 3. Instalar o plugin `poetry-plugin-export`

Este passo é **obrigatório** desde as versões recentes do Poetry
para que o comando `export` exista.

```bash
poetry self add poetry-plugin-export
```

---

## 📝 4. Ajustar o `pyproject.toml`

Garanta que seu arquivo `pyproject.toml` usa a seção `[project]` para definir a
compatibilidade de versão do Python. Isso já permite o uso do Python 3.14 e 3.15.

```toml
[project]
name = "seu-projeto"
version = "0.1.0"
...
requires-python = ">=3.10,<4.0"
...
dependencies = [
    # Suas dependências aqui
]
```

---

## ➕ 5. Adicionar pacotes (Se necessário)

Se você estiver migrando um `requirements.txt` existente para o Poetry:

### PowerShell (Windows)

```powershell
Get-Content requirements.txt | ForEach-Object { poetry add $_ }
```

### Bash/Linux/macOS

```bash
poetry add $(cat requirements.txt)
```

---

## 📤 6. Exportar para `requirements.txt`

Depois de instalar o plugin e definir suas dependências, você pode exportar.

### Apenas dependências principais

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### Incluindo dependências de desenvolvimento

```bash
poetry export -f requirements.txt --with dev --output requirements.txt --without-hashes
```

---

## 📌 Dica Final

Sempre que modificar o `pyproject.toml` ou rodar `poetry add/remove`, execute
novamente o comando `poetry export` para manter o `requirements.txt` sincronizado.

---

## 📚 Referências

- <https://python-poetry.org/docs/>
- <https://github.com/python-poetry/poetry-plugin-export>
