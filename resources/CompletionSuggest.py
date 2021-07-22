import copy

from flask_restful import reqparse, Resource
import requests

parser = reqparse.RequestParser()
parser.add_argument('key')

url_prefix = "http://10.192.105.176:9200/"


def suggest_disease(query):
    url = url_prefix + "disease/_search"
    query["suggest"]["suggester"]["completion"]["field"] = "name.suggest"
    response = requests.get(url, json=query).json()
    return response


def suggest_hospital(query):
    url = url_prefix + "hospital/_search/"
    query["suggest"]["suggester"]["completion"]["field"] = "hospital_name.suggest"
    response = requests.get(url, json=query).json()
    return response


def suggest_doctor(query):
    url = url_prefix + "doctor/_search/"
    query["suggest"]["suggester"]["completion"]["field"] = "doctor_name.suggest"
    response = requests.get(url, json=query).json()
    return response


def suggest_office(query):
    url = url_prefix + "office/_search/"
    query["suggest"]["suggester"]["completion"]["field"] = "office_name.suggest"
    response = requests.get(url, json=query).json()
    return response


class CompletionSuggest(Resource):

    def get(self, get_type):
        args = parser.parse_args()
        key = args['key']
        if get_type not in ["0", "1", "2", "3", "4"]:
            return "illegal url"

        query = {
            "_source": "",
            "suggest": {
                "suggester": {
                    "prefix": key,
                    "completion": {
                        "field": "",
                        "analyzer": "ik_smart",
                        "skip_duplicates": True
                    }
                }
            }
        }

        find_by_type = {
            '1': suggest_hospital,
            '2': suggest_doctor,
            '3': suggest_office,
            '4': suggest_disease,
        }
        res = []
        if get_type == '0':
            for i in ['1', '2', '3', '4']:
                response = find_by_type[i](query)
                for item in response["suggest"]["suggester"][0]["options"]:
                    res.append(item["text"])
        else:
            response = find_by_type[get_type](query)
            for item in response["suggest"]["suggester"][0]["options"]:
                res.append(item["text"])

        return res
