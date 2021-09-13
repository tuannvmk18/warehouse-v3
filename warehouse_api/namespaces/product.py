import json

from flask_restx import Namespace, Resource, fields, marshal
from warehouse_api.services import product as product_service

product_ns = Namespace('product', description='Product Api')

product_create_schema = product_ns.model('Product Create Schema', {
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Float(min=0, required=True)
}, strict=True)

product_update_schema = product_ns.model('Product Update Schema', {
    'id': fields.Integer(min=0, required=True),
    'name': fields.String(required=False),
    'description': fields.String(required=False),
    'price': fields.Float(min=0, required=False)
}, strict=True)

product_schema = product_ns.model('Product Schema', {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Float(min=0, required=True)
}, strict=True)

product_response_success_schema = product_ns.model('Product reponse susscess schema', {
    'data': fields.Nested(product_schema),
    'status_code': fields.Integer()
})

product_list_response_success_schema = product_ns.model('Product reponse susscess schema', {
    'data': fields.List(fields.Nested(product_schema)),
    'status_code': fields.Integer()
})

product_response_failed_schema = product_ns.model('Product reponse failded schema', {
    'error': fields.String,
    'status_code': fields.Integer
})


@product_ns.route("/")
class ProductNoParam(Resource):

    @product_ns.response(model=product_list_response_success_schema, code=200, description="Get List Product Success")
    def get(self):
        return marshal({
            'data': product_service.get_all_as_json(),
            'status_code': 200
        }, product_list_response_success_schema), 200

    @product_ns.doc(body=product_create_schema)
    @product_ns.response(model=product_response_success_schema, code=201, description="Create Product Success")
    @product_ns.expect(product_create_schema, validate=True)
    def post(self):
        product = product_service.create_as_json(product_ns.payload)
        return marshal({
            "data": json.loads(product),
            "status_code": 201
        }, product_response_success_schema), 201

    @product_ns.doc(body=product_update_schema, validate=True)
    @product_ns.expect(product_update_schema, validate=True)
    @product_ns.response(model=product_response_success_schema, code=200, description="Update Product Success")
    @product_ns.response(model=product_response_failed_schema, code=404, description="Update Product Failed")
    def put(self):
        product = product_service.update_from_json(product_ns.payload)
        if product is not None:
            return marshal({
                'data': json.loads(product),
                'status_code': 200
            }, product_response_success_schema), 200
        return marshal({
            'error': 'product not found',
            'status_code': 404
        }, product_response_failed_schema), 404


@product_ns.route("/<int:product_id>")
@product_ns.param('product_id', 'The product identifier')
class ProductParamID(Resource):

    @product_ns.response(model=product_response_success_schema, code=200, description="Get Product Success")
    @product_ns.response(model=product_response_failed_schema, code=404, description="Product Not Found")
    def get(self, product_id: int):
        product = product_service.get_as_json_by_id(product_id)
        if product is None:
            return marshal({
                'message': 'product not found',
                'status_code': 404
            }, product_response_failed_schema), 404
        return marshal({
            'data': json.loads(product),
            'status_code': 200
        }, product_response_success_schema), 200

    @product_ns.response(model=product_response_failed_schema, code=404, description="Product Not Found")
    def delete(self, product_id: int):
        if product_service.delete_by_id(product_id):
            return "", 204
        return marshal({
            "message": "product not found",
            "status_code": 404
        }, product_response_failed_schema), 404


@product_ns.route("/<int:product_id>/<action>")
class ProductAction(Resource):
    def get(self, product_id: int, action: str):
        if action == "get_all_info":
            return product_service.get_from_all_warehouse(product_id)
