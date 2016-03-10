import json
from bson import json_util
from flask_restplus import Resource


def register_routes(config, api, model):

    class Results(Resource):
        def get(self):
            response = model.get_all()
            return json.loads(json_util.dumps(response))

    api.add_resource(Results, '/i')
