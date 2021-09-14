from flask_restx import Namespace, Resource, fields, marshal
from warehouse_api.services import order as order_service

order_ns = Namespace('order', 'Order Api')


@order_ns.route('/')
class OrderNoParam(Resource):
    def get(self):
        return order_service.get_all_as_json()

    def post(self):
        order_service.create(order_ns.payload)


@order_ns.route('/<int:order_id>')
class OrderIDParam(Resource):
    def get(self, order_id: int):
        res = order_service.get_by_id_as_json(order_id)
        if res is not None:
            return {
                       'data': res,
                       'status_code': 200
                   }, 200
        return {
                   'message': 'order not found',
                   'status_code': 404
               }, 404

    def delete(self, order_id: int):
        if order_service.delete_by_id(order_id):
            return {
                       'messgae': 'OK',
                       'status_code': 200
                   }, 404
        return {
                   'error': 'order not found',
                   'status_code': 404
               }, 404
