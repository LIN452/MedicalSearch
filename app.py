#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.wrappers.request import PlainRequest
from resources.Search import Search
from resources.FindOne import FindDisease, FindHospital, FindOffice, FindDoctor
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app)
api = Api(app)

api.add_resource(Search, '/search')
api.add_resource(FindDisease, '/findOne/disease')
api.add_resource(FindHospital, '/findOne/hospital')
api.add_resource(FindOffice, '/findOne/office')
api.add_resource(FindDoctor, '/findOne/doctor')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)