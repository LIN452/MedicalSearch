#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.wrappers.request import PlainRequest
from resources.Search import Search
from resources.FindOne import FindOne
from resources.CompletionSuggest import CompletionSuggest
#from resources import Search,FindOne,CompletionSuggest
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app)
api = Api(app)

api.add_resource(Search, '/search')
api.add_resource(FindOne, '/findOne/<get_type>')
api.add_resource(CompletionSuggest, '/suggest/<get_type>')
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)
