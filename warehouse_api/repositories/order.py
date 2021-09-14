import datetime
import json
import sys
from typing import List

from sqlmodel import Session, select, text
from warehouse_api import engine
from warehouse_api.models import Order, StockQuant, OrderProductLink
from warehouse_api.ultis import update_model


def get_all():
    with Session(engine) as session:
        statement = select(Order)
        results = session.exec(statement)
        orders = results.fetchall()
        return orders


def get_by_id(warehouse_id: int):
    with Session(engine) as session:
        statement = select(Order).where(Order.id == warehouse_id)
        results = session.exec(statement)
        order = results.one_or_none()
        return order


def delete_by_id(warehouse_id: int):
    with Session(engine) as session:
        statement = select(Order).where(Order.id == warehouse_id)
        order = session.exec(statement).one_or_none()
        if order is not None:
            session.delete(order)
            session.commit()
            return True
        return False


def create(data):
    order: Order = Order()
    order.warehouse_id = data['warehouse_id']
    list_product: List[StockQuant] = []
    list_oder_product_link: List[OrderProductLink] = []
    with Session(engine) as session:
        for p in data['products']:
            statement = select(StockQuant).where(StockQuant.warehouse_id == data['warehouse_id']).where(
                StockQuant.product_id == p['product_id'])
            stock_quant = session.exec(statement).one_or_none()
            if stock_quant is None:
                return False
            if stock_quant.quantity < p['quantity']:
                return False
            stock_quant.quantity -= p['quantity']
            order_product_link: OrderProductLink = OrderProductLink()
            order_product_link.product_id = stock_quant.product_id
            order_product_link.quantity = p['quantity']
            list_oder_product_link.append(order_product_link)
            list_product.append(stock_quant)
        order.status = "draft"
        order.order_date = datetime.datetime.now()
        session.add(order)
        for p in list_product:
            session.add(p)

        session.commit()
        session.refresh(order)

        for o_p in list_oder_product_link:
            o_p.order_id = order.id
            session.add(o_p)
        session.commit()
    return True
