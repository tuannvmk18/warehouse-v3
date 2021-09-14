import json
import sys

from sqlmodel import Session, select, text
from warehouse_api import engine
from warehouse_api.models import Order
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
