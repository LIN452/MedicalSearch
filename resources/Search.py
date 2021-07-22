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
        
        if key == "":
            key = region
        
        query = {
            "query": {
                "bool":{
                    "must":[{
                        "query_string": {
                            "query": key
                        }
                    }]
                   # "should":{
                   #     "query_string": {
                   #         "query": key
                            
                    #    }
                   # }
                    
                }
            },
            "highlight": {
                "fields": {
                }
            },
            "size": pageSize,
            "from": (pageNum-1)*pageSize,
        } 

        if region != "":
            region = region.replace('市','')
            region = region.replace('省','')
            region = region.replace('区','')
            query['query']['bool']['must'].append({"match":{"hospital_address":region}})
            #query['query']['bool']['must']['match']['hospital_address']=region
            #query['query']['bool']['must'].['match']={"hospital_address":region}

        fieldlist = []
        url = "http://10.192.105.176:9200"
        
        if type == DOCTOR:
            url = url + "/doctor"
            fieldlist=['doctor_name','skill','doctor_intro','office_name2','office_name','hospital_name','hospital_address','doctor_name.pinyin']
        
        if type == HOSPITAL:
            url = url+"/hospital"
            fieldlist=['hospital_address','hospital_name','label_1','label_2','add','intro','hospital_name.pinyin']
        
        if type == OFFICE:
            url = url+"/office"
            fieldlist=['office_name','office_name2','hospital_name','office_name.pinyin','hospital_address']

        if type == DISEASE:
            url = url +"/disease"
            fieldlist=['name','desc','cause','symptom','name.pinyin']

        if type == UNLIMITED:
            fieldlist=['doctor_name','skill','doctor_intro','doctor_name.pinyin','office_name2','hospital_name.pinyin','office_name','office_name.pinyin','hospital_name','hospital_address','name.pinyin']+['hospital_address','hospital_name','label_1','label_2','add','intro']+['office_name','office_name2','hospital_name']+['name','desc','cause','symptom']
            fieldlist = list(set(fieldlist)) #去重

        url = url + "/_search"

        query["query"]['bool']['must'][0]['query_string']["fields"]=fieldlist
        for item in fieldlist:
            query["highlight"]["fields"][item]={}
        print(query)
        response = requests.get(url,json=query).json()
        res = {}
        reslist=[]
        print(response)
        total = min(response['hits']["total"]["value"],maxValue)

        res["total"]=total

        #for hit in response['hits']["hits"][(pageNum-1)*pageSize:pageNum*pageSize]:
        for hit in response['hits']["hits"]:
            item = {"info":hit["_source"]}
            item["info"]["type"]=hit["_index"]
            if "name" in item["info"]:
                item["info"]["name_origin"]=item["info"]["name"]
            for singleItem in hit["highlight"]:
                item["info"][singleItem]=''.join(hit["highlight"][singleItem])
            
            reslist.append(item)

        res["total"]=total
        res["time"]=response["took"]
        res["reslist"]=reslist

        return res

    '''def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
    '''
