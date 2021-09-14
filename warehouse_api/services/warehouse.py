import json
from typing import List

from warehouse_api.models import WareHouse, StockQuant
from warehouse_api.repositories import warehouse as warehouse_repository


def create_from_json(payload: dict):
    warehouse: WareHouse = WareHouse()
    warehouse.name = payload['name']
    warehouse.address = payload['address']
    warehouse.phone = payload['phone']

    warehouse = warehouse_repository.create(warehouse)
    return warehouse.json()


def get_all_as_json():
    results = [json.loads(warehouse.json()) for warehouse in warehouse_repository.get_all()]
    return results


def get_by_id_as_json(warehouse_id: int):
    result = warehouse_repository.get_by_id(warehouse_id)
    if result is not None:
        return result.json()
    return None


def delete_by_id(warehouse_id: int):
    return warehouse_repository.delete_by_id(warehouse_id)


def update_from_json(payload: dict):
    warehouse = warehouse_repository.update(payload)
    return warehouse


def update_product_quantity(warehouse_id: int, payload: dict):
    warehouse_id = warehouse_id
    list_stock_quant: List[StockQuant] = []
    for p in payload:
        stock_quant: StockQuant = StockQuant()
        stock_quant.warehouse_id = warehouse_id
        stock_quant.product_id = p['product_id']
        stock_quant.quantity = p['quantity']
        list_stock_quant.append(stock_quant)
    return warehouse_repository.update_product_quantity(warehouse_id, list_stock_quant)
