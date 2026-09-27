import json
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Loja API - Pedidos",
    description=(
        "API responsável por gerenciar os pedidos de uma loja online. "
        "O catálogo de produtos é consultado pelo front-end diretamente na "
        "FakeStore API; esta API cuida da persistência e do ciclo de vida "
        "dos pedidos feitos pelos clientes."
    ),
    version="1.0.0",
)

# Libera o consumo pelo front-end (ex: http://localhost:5173 em dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATUS_VALIDOS = {"pendente", "pago", "enviado", "cancelado"}


def _pedido_para_saida(db_pedido: models.Pedido) -> dict:
    """Converte o modelo do banco (itens como texto JSON) para o schema de saída."""
    return {
        "id": db_pedido.id,
        "cliente_nome": db_pedido.cliente_nome,
        "itens": json.loads(db_pedido.itens),
        "total": db_pedido.total,
        "status": db_pedido.status,
        "criado_em": db_pedido.criado_em,
    }


@app.get("/", tags=["status"])
def raiz():
    return {"mensagem": "Loja API - Pedidos. Consulte /docs para o Swagger."}


@app.post("/pedidos", response_model=schemas.PedidoOut, status_code=201, tags=["pedidos"])
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    """Cria um novo pedido a partir dos itens escolhidos no front-end."""
    if not pedido.itens:
        raise HTTPException(status_code=400, detail="O pedido precisa ter pelo menos um item.")
    db_pedido = crud.criar_pedido(db, pedido)
    return _pedido_para_saida(db_pedido)


@app.get("/pedidos", response_model=schemas.PedidoListOut, tags=["pedidos"])
def listar_pedidos(
    status: str | None = Query(default=None, description="Filtra por status do pedido"),
    pagina: int = Query(default=1, ge=1),
    tamanho_pagina: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Lista pedidos com filtro por status e paginação."""
    if status and status not in STATUS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Status inválido. Use um de: {STATUS_VALIDOS}")
    skip = (pagina - 1) * tamanho_pagina
    total_registros, resultados = crud.listar_pedidos(db, status=status, skip=skip, limit=tamanho_pagina)
    return {
        "total_registros": total_registros,
        "pagina": pagina,
        "tamanho_pagina": tamanho_pagina,
        "resultados": [_pedido_para_saida(p) for p in resultados],
    }


@app.get("/pedidos/{pedido_id}", response_model=schemas.PedidoOut, tags=["pedidos"])
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = crud.obter_pedido(db, pedido_id)
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return _pedido_para_saida(db_pedido)


@app.put("/pedidos/{pedido_id}", response_model=schemas.PedidoOut, tags=["pedidos"])
def atualizar_status(pedido_id: int, dados: schemas.PedidoUpdate, db: Session = Depends(get_db)):
    """Atualiza o status de um pedido (pendente -> pago -> enviado, ou cancelado)."""
    if dados.status not in STATUS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Status inválido. Use um de: {STATUS_VALIDOS}")
    db_pedido = crud.atualizar_status_pedido(db, pedido_id, dados.status)
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return _pedido_para_saida(db_pedido)


@app.delete("/pedidos/{pedido_id}", status_code=204, tags=["pedidos"])
def deletar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    sucesso = crud.deletar_pedido(db, pedido_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return None
