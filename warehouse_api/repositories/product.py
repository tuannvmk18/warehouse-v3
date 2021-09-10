import sys

from sqlmodel import Session, select
from warehouse_api import engine
from warehouse_api.models import Product


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


def update(product_update: Product):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == product_update.id)
        results = session.exec(statement)
        product = results.one_or_none()
        if product is not None:
            product = product_update
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
        return None
