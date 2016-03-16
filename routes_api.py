import json
from bson import json_util
from flask_restplus import (
    Resource,
    fields
)
from flask import request


def register_api_routes(config, api, model):

    class GetItems(Resource):
        def get(self):
            response = model.get_items()
            return json.loads(json_util.dumps(response))

    class GetStores(Resource):
        def get(self):
            response = model.get_stores()
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

    api.add_resource(GetItems, '/get_items')
    api.add_resource(GetStores, '/get_stores')
    api.add_resource(GetItemForStore, '/get_item_for_store')
    api.add_resource(GetAllForStore, '/get_all_for_store')
    api.add_resource(GetItemForAllStores, '/get_item_for_all_stores')
    api.add_resource(GetTimestampsForItem, '/get_timestamps_for_item')
