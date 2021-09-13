import sys
import json
from warehouse_api.repositories import product as product_repository
from warehouse_api.models import Product


def get_all_as_json(limit: int = sys.maxsize, offset: int = 0):
    products = [json.loads(product.json()) for product in product_repository.get_all(limit, offset)]
    return products


def get_as_json_by_id(product_id: int):
    product = product_repository.get_by_id(product_id)
    if product is not None:
        return json.loads(json.dumps(product.json()))
    return None


def create_as_json(payload: dict):
    product: Product = Product(name=payload['name'], description=payload['description'], price=payload['price'])
    product = product_repository.create(product)
    return json.loads(json.dumps(product.json()))


def update_from_json(payload: dict):
    product: Product = Product(id=payload['id'], name=payload['name'], description=payload['description'],
                               price=payload['price'])
    product = product_repository.update(json.loads(product.json()))
    if product is not None:
        return json.loads(json.dumps(product.json()))
    return None


def delete_by_id(product_id: int):
    return product_repository.delete_by_id(product_id)


def get_from_all_warehouse(product_id: int):
    raw_results = product_repository.get_from_all_warehouse(product_id)
    return raw_results[0][0]
