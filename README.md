# TrackFlow

API REST construída com FastAPI e **Arquitetura Orientada a Eventos (EDA)**, seguindo Clean Architecture.

## Stack

| Componente | Tecnologia |
|------------|------------|
| API        | FastAPI + Uvicorn |
| Persistência | MongoDB (Motor — driver assíncrono) |
| Mensageria | RabbitMQ (aio-pika) |
| Config     | Pydantic Settings + `.env` |

## Requisitos

- Python 3.12+
- Docker e Docker Compose (para infraestrutura local)

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

## Infraestrutura local

Suba MongoDB e RabbitMQ via Docker Compose:

```bash
docker compose up -d
```

| Serviço        | URL / Porta |
|----------------|-------------|
| MongoDB        | `mongodb://localhost:27017` |
| Mongo Express  | http://localhost:8081 |
| RabbitMQ       | `amqp://guest:guest@localhost:5672/` |
| RabbitMQ UI    | http://localhost:15672 (guest/guest) |

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
├── api/                  # Camada de apresentação (rotas HTTP)
│   └── v1/               # Endpoints versionados
├── core/                 # Configurações, dependências e lifespan
├── events/               # Publicação e consumo de eventos (EDA)
├── infrastructure/       # Adaptadores externos
│   ├── mongodb/          # Cliente assíncrono MongoDB
│   └── messaging/        # Broker RabbitMQ
├── models/               # Documentos MongoDB (Pydantic)
├── schemas/              # DTOs de entrada/saída
├── repositories/         # Acesso a dados (MongoDB)
├── services/             # Regras de negócio
├── tests/
└── main.py               # Factory FastAPI + lifespan
```

## Ciclo de vida assíncrono

A aplicação gerencia conexões via `lifespan` do FastAPI:

1. **Startup** — conecta ao MongoDB e RabbitMQ, declara o exchange de eventos
2. **Runtime** — dependências injetam `database`, `channel` e `EventPublisher`
3. **Shutdown** — fecha conexões de forma limpa

## Variáveis de ambiente

| Variável       | Descrição                          | Padrão |
|----------------|------------------------------------|--------|
| `MONGO_URI`    | URI de conexão MongoDB             | `mongodb://localhost:27017` |
| `MONGO_DB`     | Nome do banco                      | `trackflow` |
| `RABBITMQ_URI` | URI de conexão RabbitMQ            | `amqp://guest:guest@localhost:5672/` |
| `SPEED_LIMIT`  | Limite de velocidade global (km/h) | `80.0` |

Consulte `.env.example` para a lista completa.

## Testes

```bash
pytest
```

Os testes utilizam um lifespan mockado — não exigem MongoDB ou RabbitMQ em execução.

## Lint e formatação

```bash
ruff check app
ruff format app
```

## Fluxo Git

| Branch   | Propósito                                      |
|----------|------------------------------------------------|
| `master` | Código estável, pronto para produção           |
| `dev`    | Integração contínua de novas funcionalidades   |

### Workflow de desenvolvimento

1. Partir sempre da branch `dev`
2. Criar branch `feature/nome-da-feature` a partir de `dev`
3. Abrir Pull Request para `dev`
4. Após estabilização, PR de `dev` → `master`

```
master  ─────────────────────────────●──────────
                  \                 /
dev     ────●──●──●──●──●──●──●──●──●
             \    /
feature     ●──●
```
