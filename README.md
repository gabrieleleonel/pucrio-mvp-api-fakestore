# FakeStore API - Pedidos

API REST em **Python (FastAPI)** responsável por gerenciar os pedidos de uma loja online. O catálogo de produtos é consultado pelo front-end diretamente na [FakeStore API](https://fakestoreapi.com/); esta API cuida exclusivamente da persistência e do ciclo de vida dos pedidos (criação, consulta, atualização de status e cancelamento).

## Descrição do projeto

Este componente é a **API secundária/back-end** do MVP de componentização (Cenário 1). Ele expõe rotas REST consumidas pelo front-end da FakeStore (`FakeStore-frontend`), persiste os dados em **SQLite** e oferece filtro por status e paginação nas consultas.

## Modelo de dados

Um `Pedido` contém:

| Campo        | Tipo     | Descrição                                           |
| ------------ | -------- | --------------------------------------------------- |
| id           | int      | identificador do pedido                             |
| cliente_nome | string   | nome de quem fez o pedido                           |
| itens        | lista    | produtos escolhidos (id, título, preço, quantidade) |
| total        | float    | soma calculada no servidor                          |
| status       | string   | `pendente`, `pago`, `enviado` ou `cancelado`        |
| criado_em    | datetime | data de criação                                     |

## Rotas

| Método | Rota            | Descrição                                                              |
| ------ | --------------- | ---------------------------------------------------------------------- |
| POST   | `/pedidos`      | Cria um novo pedido                                                    |
| GET    | `/pedidos`      | Lista pedidos, com `?status=` e paginação (`?pagina=&tamanho_pagina=`) |
| GET    | `/pedidos/{id}` | Detalha um pedido específico                                           |
| PUT    | `/pedidos/{id}` | Atualiza o status de um pedido                                         |
| DELETE | `/pedidos/{id}` | Remove um pedido                                                       |

Documentação interativa (Swagger) disponível em `/docs` após subir a aplicação.

## Instalação e execução local (sem Docker)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`.

## Execução via Docker

```bash
docker build -t fakestore-backend .
docker run -p 8000:8000 fakestore-backend
```

A API ficará disponível em `http://localhost:8000/docs`.

## Estrutura do projeto

```
FakeStore-backend/
├── app/
│   ├── main.py        # rotas da API
│   ├── models.py      # modelo SQLAlchemy (Pedido)
│   ├── schemas.py      # schemas Pydantic de entrada/saída
│   ├── crud.py         # funções de acesso ao banco
│   └── database.py     # configuração do SQLite
├── requirements.txt
├── Dockerfile
└── README.md
```
