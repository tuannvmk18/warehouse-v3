import json
import sys

from sqlmodel import Session, select
from warehouse_api import engine
from warehouse_api.models import WareHouse


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
