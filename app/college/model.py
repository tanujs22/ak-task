import config
import json, datetime
from datetime import datetime
import time, csv
from elasticsearch import Elasticsearch

class College():

    def __init__(self):
        self.date = datetime.now().date()
        self.dt_strg = '{:%Y-%m-%d}'.format(self.date)
        self.dt_unix = time.mktime(self.date.timetuple())

    def save_college(self, csvfile):
        es = Elasticsearch(config.ES_ENDPOINT)
        reader = csv.DictReader(csvfile)
        for row in reader:
            res = es.index(index="college", doc_type='college_info', body=row)
            print res['created']
        return True

    def fetch_all(self, univ, cities, fees, marks):
        es = Elasticsearch(config.ES_ENDPOINT)
        query = "(university : '')"
        if univ:
            query = "(university : %s)" % ' OR '.join(univ)
        if cities:
            query += " OR (city : %s)"  % ' OR '.join(cities)

        body = {
                "query": {
                    "query_string": {
                        "query": query
                    }
                }
            }
        print body
        res = es.search(index="college", doc_type='college_info', body= body)
        res_list = res['hits']['hits']
        response_list = []
        for r in res_list:
            response_list.append(r['_source'])
        return response_list
    