from flask_restful import reqparse, Resource
import requests

parser = reqparse.RequestParser()
parser.add_argument('key')

url_prefix = "http://10.192.166.110:9200/"


def find_disease(key):
    url = url_prefix + "disease/disease/" + key
    response = requests.get(url).json()
    return response


def find_hospital(key):
    url = url_prefix + "hospital/hospital/" + key
    response = requests.get(url).json()
    return response


def find_doctor(key):
    url = url_prefix + "doctor/doctor/" + key
    response = requests.get(url).json()
    return response


def find_office(key):
    url = url_prefix + "office/office/" + key
    response = requests.get(url).json()
    return response


class FindOne(Resource):

    def get(self, get_type):
        args = parser.parse_args()
        key = args['key']
        if get_type not in ["1", "2", "3", "4"]:
            return "illegal url"

        find_by_type = {
            '1': find_hospital(key),
            '2': find_doctor(key),
            '3': find_office(key),
            '4': find_disease(key),
        }

        res = {}
        response = find_by_type[get_type]

        if not response["found"]:
            res["found"] = False
        else:
            res["found"] = True
            res["resp"] = {"info": response["_source"]}

        return res