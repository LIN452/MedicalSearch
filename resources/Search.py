from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.sansio.response import Response
from werkzeug.wrappers.request import PlainRequest, Request
import requests

parser = reqparse.RequestParser()
parser.add_argument('key')
parser.add_argument('type', type=int, default=0)
parser.add_argument('region', default="")
parser.add_argument('pageNum', type=int, default=1)
parser.add_argument('pageSize', type=int, default=10)

maxValue = 1000
UNLIMITED = 0
HOSPITAL = 1
DOCTOR = 2
OFFICE = 3
DISEASE = 4

class Search(Resource):
    def get(self):
        
        args = parser.parse_args()
        key = args['key']
        type = args['type']
        region = args['region']
        pageNum = args['pageNum']
        pageSize = args['pageSize']

        if region != "":
            key = str(region) +" "+str(key)
        
        query = {
            "query": {
                "query_string": {
                    "query": key
                    
                }
            },
            "highlight": {
                "fields" : {
                }
            },
            "size":maxValue
        } 

        fieldlist = []
        url = "http://10.192.166.110:9200"
        
        if type == DOCTOR:
            url = url + "/doctor"
            fieldlist=['doctor_name','skill','doctor_intro','office_name2','office_name','hospital_name','hospital_address']
        
        if type == HOSPITAL:
            url = url+"/hospital"
            fieldlist=['hospital_address','hospital_name','label_1','label_2','add','intro']
        
        if type == OFFICE:
            url = url+"/office"
            fieldlist=['office_name','office_name2','hospital_name']

        if type == DISEASE:
            url = url +"/disease"
            fieldlist=['name','desc','cause','symptom']

        if type == UNLIMITED:
            fieldlist=['doctor_name','skill','doctor_intro','office_name2','office_name','hospital_name','hospital_address']+['hospital_address','hospital_name','label_1','label_2','add','intro']+['office_name','office_name2','hospital_name']+['name','desc','cause','symptom']
            fieldlist = list(set(fieldlist)) #去重

        url = url + "/_search"

        query["query"]["query_string"]["fields"]=fieldlist
        for item in fieldlist:
            query["highlight"]["fields"][item]={}

        response = requests.get(url,json=query).json()
        res = {}
        reslist=[]
        total = min(response['hits']["total"]["value"],maxValue)

        res["total"]=total

        for hit in response['hits']["hits"][(pageNum-1)*pageSize:pageNum*pageSize]:
            item = {"info":hit["_source"]}
            item["info"]["type"]=hit["_type"]
            if "name" in hit["highlight"]:
                item["info"]["name_origin"]=item["info"]["name"]
            for singleItem in hit["highlight"]:
                item["info"][singleItem]=''.join(hit["highlight"][singleItem])
            
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
