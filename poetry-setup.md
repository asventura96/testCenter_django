# 📦 Gerenciamento de Dependências com Poetry e Exportação para requirements.txt

Este guia documenta o processo de uso do Poetry com Python 3.13 e a exportação correta para `requirements.txt`.

---

## ✅ Pré-requisitos

- Python **3.10 até 3.13** (evite versões alfa/beta como `3.14.0a3`)
- Poetry **versão 1.2+** (recomendado: `1.7+` ou `2.1+`)
- Ambiente virtual ativo (`.venv`)

---

## 🔧 1. Criar ambiente virtual com Python compatível

### Windows (PowerShell)

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

---

## 📦 2. Instalar ou atualizar o Poetry

### Se foi instalado com pip:

```bash
pip install --upgrade poetry
```

### Se foi instalado com o instalador oficial:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

---

## 🧩 3. Instalar o plugin `poetry-plugin-export`

```bash
poetry self add poetry-plugin-export
```

---

## 📝 4. Ajustar o `pyproject.toml`

No bloco `[tool.poetry.dependencies]`, defina:

```toml
[tool.poetry.dependencies]
python = "^3.13"
```

---

## ➕ 5. Adicionar pacotes a partir de `requirements.txt`

### PowerShell (Windows):

```powershell
Get-Content requirements.txt | ForEach-Object { poetry add $_ }
```

### Bash/Linux/macOS:

```bash
poetry add $(cat requirements.txt)
```

---

## 📤 6. Exportar para `requirements.txt`

### Apenas dependências principais:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### Incluindo dependências de desenvolvimento:

```bash
poetry export -f requirements.txt --with dev --output requirements.txt --without-hashes
```

---

## 📌 Dica Final

Sempre que modificar o `pyproject.toml`, execute novamente o comando de exportação para manter o `requirements.txt` atualizado.

---

## 📚 Referências

- https://python-poetry.org/docs/
- https://github.com/python-poetry/poetry-plugin-export
