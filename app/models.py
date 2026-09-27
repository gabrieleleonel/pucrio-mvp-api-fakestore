from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from .database import Base


class Pedido(Base):
    """
    Representa um pedido feito na loja.
    'itens' é armazenado como JSON serializado em texto (lista de produtos
    escolhidos no front-end, vindos originalmente do catálogo da FakeStore).
    """
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_nome = Column(String, nullable=False)
    itens = Column(Text, nullable=False)  # JSON: [{produto_id, titulo, preco, quantidade}]
    total = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="pendente")  # pendente | pago | enviado | cancelado
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
