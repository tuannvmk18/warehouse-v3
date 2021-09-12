from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class OrderStatus(str, Enum):
    draft = "draft"
    confirm = "confirm"
    done = "done"


class OrderProductLink(SQLModel, table=True):
    __tablename__ = "order_product"
    order_id: Optional[int] = Field(default=None, foreign_key="order.id", primary_key=True)
    product_id: Optional[int] = Field(default=None, foreign_key="product.id", primary_key=True)
    quantity: int

    order: "Order" = Relationship(back_populates="product_links")
    product: "Product" = Relationship(back_populates="order_links")


class StockQuant(SQLModel, table=True):
    __tablename__ = "stock_quant"

    product_id: Optional[int] = Field(default=None, foreign_key="product.id", primary_key=True)
    warehouse_id: Optional[int] = Field(default=None, foreign_key="warehouse.id", primary_key=True)
    quantity: int = Field(ge=0)

    warehouse: "WareHouse" = Relationship(back_populates="product_links")
    product: "Product" = Relationship(back_populates="warehouse_links")


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: Optional[OrderStatus] = Field(default=OrderStatus.draft)
    order_date: datetime
    warehouse_id: Optional[int] = Field(default=None, foreign_key="warehouse.id")

    product_links: List[OrderProductLink] = Relationship(back_populates="order")


class WareHouse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=120)
    address: str
    phone: str

    product_links: List[StockQuant] = Relationship(back_populates="warehouse")


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=120)
    description: str
    price: int = Field(gt=0)

    order_links: List[OrderProductLink] = Relationship(back_populates="product")
    warehouse_links: List[StockQuant] = Relationship(back_populates="product")
