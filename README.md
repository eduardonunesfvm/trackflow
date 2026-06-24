<div align="center">

# 🚛 TrackFlow

**Sistema de rastreamento de veículos em tempo real baseado em arquitetura orientada a eventos.**

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0+-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.13+-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</div>

---

## 📋 Sobre o Projeto

O **TrackFlow** é uma API backend que simula o sistema de rastreamento de frota de uma empresa de logística. Dispositivos GPS instalados nos veículos enviam periodicamente suas coordenadas, e o sistema processa essas informações de forma assíncrona, armazenando o histórico e gerando alertas automáticos.

O projeto foi desenvolvido com foco educacional, com o objetivo de consolidar na prática conceitos de **mensageria**, **bancos NoSQL**, **processamento assíncrono** e **arquitetura orientada a eventos (EDA)**.

> Não há frontend. Toda comunicação ocorre via API REST.

---

## 🏗️ Arquitetura

O sistema segue o padrão **Event-Driven Architecture (EDA)**. A API nunca persiste localizações diretamente — ela valida os dados recebidos, publica um evento na fila e retorna imediatamente. O processamento acontece de forma assíncrona via consumers.

```
GPS Device → FastAPI → RabbitMQ → Consumer → MongoDB
```

### Filas RabbitMQ

| Fila | Responsabilidade |
|------|-----------------|
| `gps.location.received` | Recebe novas localizações publicadas pela API |
| `gps.location.dlq` | Dead Letter Queue — armazena mensagens que falharam no processamento |

### Camadas da Aplicação

```
├── Routes       → Recebe requisições HTTP e retorna respostas
├── Services     → Contém regras de negócio e orquestra operações
└── Repositories → Responsável pela comunicação com o banco de dados
```

---

## 🛠️ Tecnologias

| Categoria | Tecnologia |
|-----------|-----------|
| Linguagem | Python 3.13+ |
| Framework | FastAPI + Pydantic |
| Mensageria | RabbitMQ + Pika |
| Banco de Dados | MongoDB + Motor (async) |
| Infraestrutura | Docker + Docker Compose |

---

## 📦 Modelagem do Banco de Dados

### Collection `vehicles`
```json
{
  "_id": "ObjectId",
  "plate": "ABC1D23",
  "model": "Volkswagen Delivery",
  "active": true,
  "created_at": "2026-06-24T10:00:00"
}
```

### Collection `locations`
```json
{
  "_id": "ObjectId",
  "vehicle_id": "ObjectId",
  "latitude": -20.443,
  "longitude": -54.647,
  "speed": 70,
  "timestamp": "2026-06-24T10:00:00"
}
```

### Collection `alerts`
```json
{
  "_id": "ObjectId",
  "vehicle_id": "ObjectId",
  "type": "SPEED_LIMIT_EXCEEDED",
  "speed": 110,
  "created_at": "2026-06-24T10:00:00"
}
```

---

## 🔌 Endpoints

### Veículos

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/v1/vehicles` | Cadastrar novo veículo |
| `GET` | `/api/v1/vehicles` | Listar todos os veículos |
| `GET` | `/api/v1/vehicles/{id}` | Buscar veículo por ID |

### Localizações

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/v1/locations` | Receber nova localização (publica na fila) |
| `GET` | `/api/v1/vehicles/{id}/last-location` | Última localização do veículo |
| `GET` | `/api/v1/vehicles/{id}/history` | Histórico completo de localizações |

### Alertas

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/v1/vehicles/{id}/alerts` | Listar alertas do veículo |

### Sistema

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/health` | Health check da aplicação |

---

## 🚀 Como Executar

### Pré-requisitos

- [Docker](https://www.docker.com/) instalado
- [Docker Compose](https://docs.docker.com/compose/) instalado

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/trackflow.git
cd trackflow
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` conforme necessário:

```env
MONGO_URI=mongodb://mongo:27017
MONGO_DB=trackflow
RABBITMQ_URI=amqp://guest:guest@rabbitmq:5672/
SPEED_LIMIT=80
```

### 3. Suba os serviços

```bash
docker compose up --build
```

A API estará disponível em `http://localhost:8000`.

A documentação interativa (Swagger) estará em `http://localhost:8000/docs`.

---

## 📁 Estrutura do Projeto

```
trackflow/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/
│   │       │   ├── vehicles.py
│   │       │   ├── locations.py
│   │       │   └── alerts.py
│   │       └── router.py
│   ├── core/
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── db/
│   │   └── mongo.py
│   ├── messaging/
│   │   ├── publisher.py
│   │   └── consumer.py
│   ├── models/
│   │   ├── vehicle.py
│   │   ├── location.py
│   │   └── alert.py
│   ├── repositories/
│   │   ├── vehicle_repository.py
│   │   ├── location_repository.py
│   │   └── alert_repository.py
│   ├── services/
│   │   ├── vehicle_service.py
│   │   ├── location_service.py
│   │   └── alert_service.py
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚙️ Funcionalidades

- [x] Cadastro e gestão de veículos da frota
- [x] Recebimento de coordenadas GPS via API REST
- [x] Publicação de eventos no RabbitMQ (processamento assíncrono)
- [x] Persistência de localizações via consumer
- [x] Consulta de última localização e histórico por período
- [x] Detecção automática de excesso de velocidade com geração de alertas
- [x] Dead Letter Queue (DLQ) para mensagens com falha
- [x] Retry automático no consumer
- [x] Tratamento global de exceções
- [x] Logging estruturado
- [x] Containerização completa com Docker Compose

---

## 🎯 Conceitos Estudados

| Conceito | Como é aplicado no projeto |
|----------|--------------------------|
| **Event-Driven Architecture** | A API publica eventos; consumers reagem a eles de forma independente |
| **Mensageria com RabbitMQ** | Desacoplamento entre produção e processamento de dados |
| **Dead Letter Queue** | Mensagens com falha são redirecionadas para a DLQ sem perda |
| **MongoDB** | Persistência flexível com collections para veículos, localizações e alertas |
| **Processamento Assíncrono** | A API responde imediatamente; consumers processam em background |
| **Arquitetura em Camadas** | Separação clara entre Routes, Services e Repositories |
| **Princípios SOLID** | Responsabilidade única e inversão de dependência nas camadas |
| **Containerização** | Todos os serviços sobem com um único `docker compose up` |

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
