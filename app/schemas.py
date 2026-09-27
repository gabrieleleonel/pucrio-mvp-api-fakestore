from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ItemPedido(BaseModel):
    produto_id: int
    titulo: str
    preco: float
    quantidade: int = Field(gt=0)


class PedidoCreate(BaseModel):
    cliente_nome: str
    itens: List[ItemPedido]


class PedidoUpdate(BaseModel):
    status: str = Field(
        description="Um de: pendente, pago, enviado, cancelado"
    )


class PedidoOut(BaseModel):
    id: int
    cliente_nome: str
    itens: List[ItemPedido]
    total: float
    status: str
    criado_em: datetime

    class Config:
        from_attributes = True


class PedidoListOut(BaseModel):
    total_registros: int
    pagina: int
    tamanho_pagina: int
    resultados: List[PedidoOut]
