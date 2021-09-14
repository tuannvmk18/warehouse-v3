import sys
import json
from warehouse_api.repositories import order as order_repository
from warehouse_api.models import Order


def get_all_as_json():
    results = [json.loads(order.json()) for order in order_repository.get_all()]
    return results


def get_by_id_as_json(order_id: int):
    order = order_repository.get_by_id(order_id)
    return order.json()


def create(data: dict):
    print("OK")
