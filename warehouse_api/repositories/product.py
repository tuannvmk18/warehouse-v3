import json
import sys

from sqlmodel import Session, select, text
from warehouse_api import engine
from warehouse_api.models import Product, StockQuant
from warehouse_api.ultis import update_model


def get_all(limit: int = sys.maxsize, offset: int = 0):
    with Session(engine) as session:
        statement = select(Product).limit(limit).offset(offset)
        results = session.exec(statement)
        products = results.fetchall()
        return products


def get_by_id(product_id: int):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == product_id)
        results = session.exec(statement)
        product = results.one_or_none()
        return product


def create(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


def delete_by_id(product_id: int):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == product_id)
        results = session.exec(statement)
        product = results.one_or_none()
        if product is not None:
            session.delete(product)
            session.commit()
            return True
        return False


def update(product_update: dict):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == product_update['id'])
        results = session.exec(statement)
        product = results.one_or_none()
        if product is not None:
            update_model(product, product_update)
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
        return None


def get_from_all_warehouse(product_id: int):
    query = text("SELECT json_build_object(\n"
                 "    'id', p.id,\n"
                 "    'name', p.name,\n"
                 "    'description', p.description,\n"
                 "    'price', p.price,\n"
                 "    'stock_quant', json_agg(json_build_object(\n"
                 "        'warehouse_id', sq.warehouse_id,\n"
                 "        'warehouse_name', w.name,\n"
                 "        'quantity', sq.quantity\n"
                 "            ))\n"
                 "           )\n"
                 "FROM product p, stock_quant sq, warehouse w\n"
                 "WHERE p.id = 1 AND sq.product_id = p.id AND sq.warehouse_id = w.id\n"
                 "GROUP BY p.description, p.price, p.name, p.id")
    with Session(engine) as session:
        results = session.execute(query, {'id': product_id})
        return results.fetchall()
