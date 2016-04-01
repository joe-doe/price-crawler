import json
from bson import json_util
from flask_restplus import (
    Resource,
    fields
)
from flask import request


def register_api_routes(api, model):

    class GetAllItems(Resource):
        def get(self):
            response = model.get_all_items()
            return json.loads(json_util.dumps(response))

    class GetAllStores(Resource):
        def get(self):
            response = model.get_all_stores()
            return json.loads(json_util.dumps(response))

    class GetStoresForItem(Resource):
        request_model = api.model('request_gsfi', {
            'item': fields.String(description='Item name', required=True)
        })

        @api.doc(body=request_model)
        def post(self):
            item = request.get_json()['item']

            response = model.get_stores_for_item(item)
            return json.loads(json_util.dumps(response))

    class GetItemForStore(Resource):
        request_model = api.model('request_gifs', {
            'item': fields.String(description='Item name', required=True),
            'store': fields.String(description='Store name', required=True)
        })

        @api.doc(body=request_model)
        def post(self):
            data = request.get_json()
            store = data['store']
            item = data['item']

            response = model.get_item_for_store(item, store)
            return json.loads(json_util.dumps(response))

    class GetAllForStore(Resource):
        request_model = api.model('request_gafs', {
            'store': fields.String(description='Store name', required=True)
        })

        @api.doc(body=request_model)
        def post(self):
            store = request.get_json()['store']

            response = model.get_all_for_store(store)
            return json.loads(json_util.dumps(response))

    class GetItemForAllStores(Resource):
        request_model = api.model('request_gifas', {
            'item': fields.String(description='Item name', required=True)
        })

        @api.doc(body=request_model)
        def post(self):
            item = request.get_json()['item']

            response = model.get_item_for_all_stores(item)
            return json.loads(json_util.dumps(response))

    class GetTimestampsForItem(Resource):
        request_model = api.model('request_gtfi', {
            'item': fields.String(description='Item name', required=True)
        })

        @api.doc(body=request_model)
        def post(self):
            item = request.get_json()['item']

            response = model.get_timestamps_for_item(item)
            return json.loads(json_util.dumps(response))

    class StoreItem(Resource):
        request_model = api.model('request_si', {
            'item': fields.String(description='Item name', required=True),
            'stores': fields.String(description='Stores in JSON', required=True)
        })

        @api.doc(body=request_model)
        def post(self):
            data = request.get_json()

            response = model.add_new_item(data)
            return json.loads(json_util.dumps(response))

    class GetSpecsForItem(Resource):
        request_model = api.model('request_gspfi', {
            'item': fields.String(description='Item name', required=True)
        })

        @api.doc(body=request_model)
        def post(self):
            item = request.get_json()['item']

            response = model.get_specs(item)
            return response

    class GetQuickSpecsForItem(Resource):
        request_model = api.model('request_gqspfi', {
            'item': fields.String(description='Item name', required=True)
        })

        @api.doc(body=request_model)
        def post(self):
            item = request.get_json()['item']

            response = model.get_quick_specs(item)
            return response

    api.add_resource(GetAllItems, '/get_items')
    api.add_resource(GetAllStores, '/get_stores')
    api.add_resource(GetItemForStore, '/get_item_for_store')
    api.add_resource(GetStoresForItem, '/get_stores_for_item')
    api.add_resource(GetAllForStore, '/get_all_for_store')
    api.add_resource(GetItemForAllStores, '/get_item_for_all_stores')
    api.add_resource(GetTimestampsForItem, '/get_timestamps_for_item')
    api.add_resource(StoreItem, '/store_item')
    api.add_resource(GetSpecsForItem, '/get_specs_for_item')
    api.add_resource(GetQuickSpecsForItem, '/get_quick_specs_for_item')
