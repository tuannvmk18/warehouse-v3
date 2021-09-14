import sys
import json
from warehouse_api.repositories import order as order_repository
from warehouse_api.models import Order


def get_all_as_json():
    results = [json.loads(order.json()) for order in order_repository.get_all()]
    return results


def get_by_id_as_json(order_id: int):
    order = order_repository.get_by_id(order_id)
    if order is not None:
        return json.loads(order.json())
    return None


def delete_by_id(order_id: int):
    return order_repository.delete_by_id(order_id)


def create(data: dict):
    return order_repository.create(data)
