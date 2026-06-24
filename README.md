# TrackFlow

API REST construída com FastAPI, seguindo Clean Architecture.

## Requisitos

- Python 3.13+
- pip

## Instalação

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements-dev.txt
cp .env.example .env
pre-commit install
```

## Executar a aplicação

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`.

## Documentação

| Recurso   | URL                          |
|-----------|------------------------------|
| Swagger   | http://127.0.0.1:8000/docs   |
| ReDoc     | http://127.0.0.1:8000/redoc  |
| OpenAPI   | http://127.0.0.1:8000/openapi.json |
| Health    | http://127.0.0.1:8000/health |

## Estrutura do projeto

```
app/
├── api/              # Camada de apresentação (rotas HTTP)
│   └── v1/           # Endpoints versionados
├── core/             # Configurações e dependências
├── models/           # Modelos SQLAlchemy (ORM)
├── schemas/          # Schemas Pydantic (DTOs)
├── repositories/     # Acesso a dados
├── services/         # Regras de negócio
├── database/         # Engine, sessão e Base ORM
├── tests/            # Testes automatizados
└── main.py           # Ponto de entrada FastAPI
```

## Migrações (Alembic)

```bash
# Criar nova migração
alembic revision --autogenerate -m "descricao"

# Aplicar migrações
alembic upgrade head
```

## Testes

```bash
pytest
```

## Lint e formatação

```bash
ruff check app
ruff format app
```

## Fluxo Git

Este projeto utiliza duas branches principais:

| Branch   | Propósito                                      |
|----------|------------------------------------------------|
| `master` | Código estável, pronto para produção           |
| `dev`    | Integração contínua de novas funcionalidades   |

### Workflow de desenvolvimento

1. Partir sempre da branch `dev`:
   ```bash
   git checkout dev
   git pull origin dev
   ```

2. Criar uma branch de feature a partir de `dev`:
   ```bash
   git checkout -b feature/nome-da-feature
   ```

3. Desenvolver, commitar e abrir Pull Request para `dev`.

4. Após revisão e testes, mesclar na `dev`.

5. Quando a `dev` estiver estável, abrir Pull Request de `dev` → `master` para release.

```
master  ─────────────────────────────●──────────
                  \                 /
dev     ────●──●──●──●──●──●──●──●──●
             \    /
feature     ●──●
```

## Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste conforme necessário. Consulte o arquivo para a lista completa de variáveis.
