from flask_restx import Namespace, Resource, fields, marshal
from warehouse_api.services import order as order_service

order_ns = Namespace('order', 'Order Api')


@order_ns.route('/')
class OrderNoParam(Resource):
    def get(self):
        return order_service.get_all_as_json()
