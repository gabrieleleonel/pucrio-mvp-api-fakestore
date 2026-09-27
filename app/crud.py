import json
from typing import Optional
from sqlalchemy.orm import Session

from . import models, schemas


def criar_pedido(db: Session, pedido: schemas.PedidoCreate) -> models.Pedido:
    total = sum(item.preco * item.quantidade for item in pedido.itens)
    itens_json = json.dumps([item.model_dump() for item in pedido.itens])

    db_pedido = models.Pedido(
        cliente_nome=pedido.cliente_nome,
        itens=itens_json,
        total=round(total, 2),
        status="pendente",
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


def listar_pedidos(
    db: Session, status: Optional[str] = None, skip: int = 0, limit: int = 10
):
    query = db.query(models.Pedido)
    if status:
        query = query.filter(models.Pedido.status == status)
    total_registros = query.count()
    resultados = (
        query.order_by(models.Pedido.criado_em.desc()).offset(skip).limit(limit).all()
    )
    return total_registros, resultados


def obter_pedido(db: Session, pedido_id: int) -> Optional[models.Pedido]:
    return db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()


def atualizar_status_pedido(
    db: Session, pedido_id: int, novo_status: str
) -> Optional[models.Pedido]:
    db_pedido = obter_pedido(db, pedido_id)
    if not db_pedido:
        return None
    db_pedido.status = novo_status
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


def deletar_pedido(db: Session, pedido_id: int) -> bool:
    db_pedido = obter_pedido(db, pedido_id)
    if not db_pedido:
        return False
    db.delete(db_pedido)
    db.commit()
    return True
