import json

from flask_restx import Namespace, Resource, fields, marshal
from warehouse_api.services import warehouse as warehouse_service

warehouse_ns = Namespace('warehouse', description='Warehouse Api')

warehouse_schema = warehouse_ns.model('Warehouse Schema', {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'phone': fields.String
}, strict=True)

warehouse_create_schema = warehouse_ns.model('Warehouse Create Schema', {
    'name': fields.String(required=True),
    'address': fields.String(required=True),
    'phone': fields.String(required=True)
}, strict=True)

warehouse_update_schema = warehouse_ns.model('Warehouse Update Schema', {
    'id': fields.Integer(required=True),
    'name': fields.String,
    'address': fields.String,
    'phone': fields.String
}, strict=True)

warehouse_response_success = warehouse_ns.model('Warehouse Response Success', {
    'data': fields.Nested(warehouse_schema),
    'status_code': fields.Integer
})

warehouse_list_response_success = warehouse_ns.model('Warehouse Response Success', {
    'data': fields.List(fields.Nested(warehouse_schema)),
    'status_code': fields.Integer
})

warehouse_response_failed = warehouse_ns.model('Warehouse Response Faild', {
    'message': fields.String,
    'status_code': fields.Integer
})

warehouse_response_delete_success = warehouse_ns.model('Warehouse Response Delete Success', {
    'message': fields.String,
    'status_code': fields.Integer
})


@warehouse_ns.route('/')
class WareHouseNoParam(Resource):
    @warehouse_ns.response(model=warehouse_list_response_success, code=200, description="Get All Warehouse")
    def get(self):
        response = warehouse_service.get_all_as_json()
        return marshal({
            'data': response,
            'status_code': 200
        }, warehouse_list_response_success), 200

    @warehouse_ns.doc(body=warehouse_create_schema)
    @warehouse_ns.expect(warehouse_create_schema, validate=True)
    @warehouse_ns.response(model=warehouse_response_success, code=201, description="Create Warehouse Success")
    def post(self):
        warehouse = warehouse_service.create_from_json(payload=warehouse_ns.payload)
        return marshal({
            'data': json.loads(warehouse),
            'status_code': 201
        }, warehouse_response_success), 201

    @warehouse_ns.doc(body=warehouse_update_schema)
    @warehouse_ns.expect(warehouse_update_schema, validate=True)
    @warehouse_ns.response(model=warehouse_response_success, code=200, description="Update Warehouse Success")
    @warehouse_ns.response(model=warehouse_response_failed, code=404, description="Warehouse not found")
    def put(self):
        print(warehouse_ns.payload)
        warehouse = warehouse_service.update_from_json(warehouse_ns.payload)
        if warehouse is not None:
            return marshal({
                'data': json.loads(warehouse.json()),
                'status_code': 200
            }, warehouse_response_success), 200
        return marshal({
            'messgae': 'warehouse not found',
            'status_code': 404
        }), 404


@warehouse_ns.route('/<int:warehouse_id>')
class WarehouseWithID(Resource):
    @warehouse_ns.response(model=warehouse_response_success, code=200, description="Get Warehouse")
    @warehouse_ns.response(model=warehouse_response_failed, code=404, description="Warehouse Not Found")
    def get(self, warehouse_id: int):
        warehouse = warehouse_service.get_by_id_as_json(warehouse_id)
        if warehouse is not None:
            return marshal({
                'data': json.loads(warehouse),
                'status_code': 200
            }, warehouse_response_success), 200
        return marshal({
            'message': 'resource not found',
            'status_code': 404
        }, warehouse_response_failed), 404

    @warehouse_ns.response(model=warehouse_response_failed, code=404, description="Warehouse Not Found")
    @warehouse_ns.response(model=warehouse_response_delete_success, code=204, description="Warehouse Deleted")
    def delete(self, warehouse_id: int):
        if warehouse_service.delete_by_id(warehouse_id):
            return {
                'message': 'resource deleted successfully',
                'status_code': 204
            }
        return marshal({
            'message': 'resource not found',
            'status_code': 404
        }, warehouse_response_failed), 404


@warehouse_ns.route('/<int:warehouse_id>/<action>')
class WarehouseAction(Resource):
    def post(self, warehouse_id: int, action: str):
        if action == "update_product_quantity":
            warehouse_service.update_product_quantity(warehouse_id=warehouse_id,payload=warehouse_ns.payload)
