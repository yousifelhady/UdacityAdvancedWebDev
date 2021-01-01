from flask import Flask, jsonify
from flask_cors import CORS
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    #if not in testing mode
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    #create the instance path dir
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    CORS(app)
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def hello():
        #return a JSON response (it has to be a response)
        return jsonify({'message': 'Hello World!'})

    @app.route('/smiley')
    def smiley():
        return ':)'

    return app