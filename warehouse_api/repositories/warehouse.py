import json
import sys
from typing import List

from sqlmodel import Session, select
from warehouse_api import engine
from warehouse_api.models import WareHouse, StockQuant
from warehouse_api.ultis import update_model


def get_all():
    with Session(engine) as session:
        statement = select(WareHouse)
        warehouses = session.exec(statement).fetchall()
        return warehouses


def create(warehouse: WareHouse):
    with Session(engine) as session:
        session.add(warehouse)
        session.commit()
        session.refresh(warehouse)
        return warehouse


def update(warehouse_update: dict):
    with Session(engine) as session:
        statement = select(WareHouse).where(WareHouse.id == warehouse_update['id'])
        warehouse = session.exec(statement).one_or_none()
        if warehouse is not None:
            update_model(warehouse, warehouse_update)
            session.add(warehouse)
            session.commit()
            session.refresh(warehouse)
            return warehouse
        return None


def get_by_id(warehouse_id: int):
    with Session(engine) as session:
        statement = select(WareHouse).where(WareHouse.id == warehouse_id)
        warehouse = session.exec(statement).one_or_none()
        return warehouse


def delete_by_id(warehouse_id: int):
    with Session(engine) as session:
        statement = select(WareHouse).where(WareHouse.id == warehouse_id)
        warehouse = session.exec(statement).one_or_none()
        if warehouse is not None:
            session.delete(warehouse)
            session.commit()
            return True
        return False


def update_product_quantity(warehouse_id: int, list_stock_quant: List[StockQuant]):
    with Session(engine) as session:
        statement = select(WareHouse).where(WareHouse.id == warehouse_id)
        warehouse = session.exec(statement).one_or_none()
        if warehouse is not None:
            for stock_quant in list_stock_quant:
                query = select(StockQuant).where(StockQuant.product_id == stock_quant.product_id).where(
                    StockQuant.warehouse_id == stock_quant.warehouse_id)
                res = session.exec(query).one_or_none()
                if res is not None:
                    update_model(res, json.loads(stock_quant.json()))
                    session.add(res)
                    session.commit()
        return True
    return False
