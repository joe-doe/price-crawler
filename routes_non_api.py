from flask import render_template


def register_non_api_routes(config, app, model):

    @app.route('/index')
    def index():
        return render_template('index.html', items=model.get_items())
