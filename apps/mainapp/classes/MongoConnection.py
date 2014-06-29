from pymongo import MongoClient
import pymongo
import json
from bson import json_util


class MongoConnection():
    def __init__(self, host="localhost", port=27017, db_name='indexer'):
        self.host = host
        self.port = port
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[db_name]

    def ensure_index(self, table_name, index=None):
        self.db[table_name].ensure_index([(index, pymongo.GEOSPHERE)])

    def create_table(self, table_name, index=None):
        self.db[table_name].create_index([(index, pymongo.DESCENDING)])

    def get_one(self, table_name, conditions={}):
        single_doc = self.db[table_name].find_one(conditions)
        json_doc = json.dumps(single_doc, default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(json_doc)

    def get_all(self, table_name, conditions={}, fields=None,
                sort_index='_id', limit=200):
        all_doc = self.db[table_name].find(conditions, fields).sort(
            sort_index, pymongo.ASCENDING).limit(limit)
        json_doc = json.dumps(list(all_doc), default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(str(json_doc))

    def insert_one(self, table_name, value):
        self.db[table_name].insert(value)

    def update_push(self, table_name, where, what):
        self.db[table_name].update(where, {"$push": what}, upsert=False)

    def update_upsert_push(self, table_name, where, what):
        self.db[table_name].update(where, {"$push": what}, upsert=True)

    def update(self, table_name, where, what):
        self.db[table_name].update(where, {"$set": what}, upsert=False)

    def update_multi(self, table_name, where, what):
        self.db[table_name].update(where, {"$set": what}, upsert=False,
                                   multi=True)

    def update_upsert(self, table_name, where, what):
        self.db[table_name].update(where, {"$set": what}, upsert=True)

    def map_reduce(self, table_name, mapper, reducer,
                   query, sort=-1, limit=20):
        if sort == 1:
            sort_direction = pymongo.ASCENDING
        else:
            sort_direction = pymongo.DESCENDING
        myresult = self.db[table_name].map_reduce(mapper, reducer,
                                                  'results', query)
        results = self.db['results'].find().sort(
            "value", sort_direction).limit(limit)
        json_doc = json.dumps(list(results), default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(str(json_doc))

    def map_reduce_search(self, table_name, mapper, reducer, query, sort_by,
                          sort=-1, limit=20):

        if sort_by == "distance":
            sort_direction = pymongo.ASCENDING
        else:
            sort_direction = pymongo.DESCENDING
        myresult = self.db[table_name].map_reduce(mapper, reducer,
                                                  'results', query)
        results = self.db['results'].find().sort("value." + sort_by,
                                                 sort_direction).limit(limit)
        json_doc = json.dumps(list(results), default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(str(json_doc))

    def aggregrate_all(self, table_name, conditions={}):
        all_doc = self.db[table_name].aggregate(conditions)['result']
        json_doc = json.dumps(list(all_doc), default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(str(json_doc))

    def group(self, table_name, key, condition, initial, reducer):
        all_doc = self.db[table_name].group(key=key, condition=condition,
                                            initial=initial, reduce=reducer)
        json_doc = json.dumps(list(all_doc), default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(str(json_doc))

    def get_distinct(self, table_name, distinct_val, query):
        all_doc = self.db[table_name].find(query).distinct(distinct_val)
        count = len(all_doc)
        parameter = {}
        parameter['count'] = count
        parameter['results'] = all_doc
        return parameter

    def get_all_vals(self, table_name, conditions={}, sort_index='_id'):
        all_doc = self.db[table_name].find(conditions).sort(
            sort_index, pymongo.DESCENDING)
        json_doc = json.dumps(list(all_doc), default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(json_doc)

    def get_paginated_values(self, table_name, conditions={}, fields={}, sort_index='_id', pageNumber=1):
        all_doc = self.db[table_name].find(conditions).sort(
            sort_index, pymongo.ASCENDING).skip(
            (pageNumber - 1) * 13).limit(13)
        json_doc = json.dumps(list(all_doc), default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(json_doc)

    def get_count(self, table_name, conditions={},fields={}, sort_index='_id'):
        return self.db[table_name].find(conditions, fields).count()
