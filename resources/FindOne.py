from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.sansio.response import Response
from werkzeug.wrappers.request import PlainRequest, Request
import requests

parser = reqparse.RequestParser()
parser.add_argument('id')

url_prefix = "http://192.168.0.116:9200/"

class FindDisease(Resource):
    def get(self):
        args = parser.parse_args()
        key = args['id']

        url = url_prefix + "disease/disease/" + key

        response = requests.get(url).json()
        print(response)

        res = {}
        if not response["found"]:
            res["found"] = False
        else:
            res["found"] = True
            res["resp"] = {"info": response["_source"]}

        return res

class FindHospital(Resource):
    def get(self):
        args = parser.parse_args()
        key = args['id']

        url = url_prefix + "hospital/hospital/" + key

        response = requests.get(url).json()
        print(response)

        res = {}
        if not response["found"]:
            res["found"] = False
        else:
            res["found"] = True
            res["resp"] = {"info": response["_source"]}

        return res

class FindOffice(Resource):
    def get(self):
        args = parser.parse_args()
        key = args['id']

        url = url_prefix + "office/office/" + key

        response = requests.get(url).json()
        print(response)

        res = {}
        if not response["found"]:
            res["found"] = False
        else:
            res["found"] = True
            res["resp"] = {"info": response["_source"]}

        return res



class FindDoctor(Resource):
    def get(self):
        args = parser.parse_args()
        key = args['id']

        url = url_prefix + "doctor/doctor/" + key

        response = requests.get(url).json()
        print(response)

        res = {}
        if not response["found"]:
            res["found"] = False
        else:
            res["found"] = True
            res["resp"] = {"info": response["_source"]}

        return res
