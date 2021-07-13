from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.sansio.response import Response
from werkzeug.wrappers.request import PlainRequest, Request
import requests

parser = reqparse.RequestParser()
parser.add_argument('key')
parser.add_argument('type')
parser.add_argument('region')

maxValue = 1000
class Search(Resource):
    def get(self):
        
        args = parser.parse_args()
        key = args['key']
        type = args['type']
        region = args['region']

        if region != "":
            key = str(region) +" "+str(key)
        
       # if type == 4:
        query = {
            "query": {
                "query_string": {
                    "query": key,
                    "default_field": "desc"
                }
            },
            "highlight": {
                "fields" : {
                    "desc" : {}
                    
                }
            },
            "size":maxValue
        }  

        response = requests.get("http://10.192.166.110:9200/_search",json=query).json()
        res = {}
        reslist=[]
        total = min(response['hits']["total"]["value"],maxValue)

        res["total"]=total
        
        for hit in response['hits']["hits"]:
            item = {"info":hit["_source"],"highlight":hit["highlight"]}
            reslist.append(item)

        res["total"]=total
        res["reslist"]=reslist
        return res

    '''def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
    '''
