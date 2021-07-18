import copy

from flask_restful import reqparse, Resource
import requests

parser = reqparse.RequestParser()
parser.add_argument('key')

url_prefix = "http://localhost:9200/"

def suggest_all(query):
    url = url_prefix + "/_search"
    #doctor = copy.deepcopy(query["suggest"]["suggester"])
    hospital = copy.deepcopy(query["suggest"]["suggester"])
    disease = copy.deepcopy(query["suggest"]["suggester"])
    office = copy.deepcopy(query["suggest"]["suggester"])
    #doctor["completion"]["field"] = "doctor_name.suggest"
    hospital["completion"]["field"] = "hospital_name.suggest"
    disease["completion"]["field"] = "name.suggest"
    office["completion"]["field"] = "office_name.suggest"

    all_query = {
        "_source": "",
        "suggest": {
            "hospital": hospital,
            #"doctor": doctor,
            #"disease": disease,
            "office": office
        }
    }
    print(all_query)
    response = requests.get(url, json=all_query).json()

    return response

def suggest_disease(query):
    url = url_prefix + "com_disease/_search"
    query["suggest"]["suggester"]["completion"]["field"] = "name.suggest"
    response = requests.get(url, json=query).json()
    return response


def suggest_hospital(query):
    url = url_prefix + "com_hospital/_search/"
    query["suggest"]["suggester"]["completion"]["field"] = "hospital_name.suggest"
    response = requests.get(url, json=query).json()
    return response


def suggest_doctor(query):
    url = url_prefix + "com_doctor/_search/"
    query["suggest"]["suggester"]["completion"]["field"] = "doctor_name.suggest"
    response = requests.get(url, json=query).json()
    return response


def suggest_office(query):
    url = url_prefix + "com_office/_search/"
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
                        "analyzer": "ik_smart"
                    }
                }
            }
        }

        find_by_type = {
            '0': suggest_all,
            '1': suggest_hospital,
            '2': suggest_doctor,
            '3': suggest_office,
            '4': suggest_disease,
        }

        res = []
        response = find_by_type[get_type](query)
        #return response
        for item in response["suggest"]["suggester"][0]["options"]:
            res.append(item["text"])

        return res
