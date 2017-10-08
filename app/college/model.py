import config
from wrappers.Mongo import init
import json, datetime
from datetime import datetime
import time
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

class Car():

    def __init__(self):
        self.date = datetime.now().date()
        self.dt_strg = '{:%Y-%m-%d}'.format(self.date)
        self.dt_unix = time.mktime(self.date.timetuple())

    def save_car(self, manufacturer, model, color, yob, rto_reg, fuel_type, cost_price, selling_price, car_for, status):
        conn = init()
        db = conn.innovaccer
        coll = db.cars
        data = {"manufacturer" : manufacturer, "model" : model, "color" : color, "yob" : yob, "rto_reg" : rto_reg, "fuel_type" : fuel_type, 'date_of_list_human' : self.dt_strg, 'date_of_list_unix' : self.dt_unix, 'cost_price' : cost_price, 'selling_price' :  selling_price, 'car_for' : car_for, "status" : status}
        try:
            car_id = coll.car_info.insert_one(data).inserted_id
            print car_id
            if car_id:
                return {'success': str(car_id)}
        except DuplicateKeyError, e:
            print e
            return {'error' : 'Registration number exist'}

    def fetch_all(self,list_type):
        conn = init()
        db = conn.innovaccer
        coll = db.cars
        if list_type:
            response = coll.car_info.find({"car_for" : list_type})
        else:
            response = coll.car_info.find()
        response_list = []
        for res in response:
            id = str(res['_id'])
            res['_id'] = id
            response_list.append(res)
        return response_list

    def fetch_one(self, car_id):
        conn = init()
        db = conn.innovaccer
        coll = db.cars
        try:
            response = coll.car_info.find_one({"_id" : ObjectId(car_id)})
            response['_id'] = car_id
            return response
        except:
            return False

    def sl_car(self, car_id, selling_price):
        conn = init()
        db = conn.innovaccer
        coll = db.cars
        try:
            response = coll.car_info.update({"_id" : ObjectId(car_id)},{"$set" : {"selling_price": selling_price, "status" : "sold"}})
            print response
            return True
        except:
            return False

    def rt_car(self, car_id, rent, origin, destination):
        conn = init()
        db = conn.innovaccer
        coll = db.cars
        data = {"_id" : car_id, "rent_data" : [{"fare" : rent, "date_of_rent_human" : self.dt_strg, 'date_of_rent_unix' : self.dt_unix}]}
        try:
            response = coll.car_rent.update({"_id" : ObjectId(car_id)},{'$push' : { "rent_data" : {"fare" : rent, "date_of_rent_human" : self.dt_strg, 'date_of_rent_unix' : self.dt_unix, "origin" : origin, "destination" : destination}}},upsert=True)
            coll.car_info.update({"_id" : ObjectId(car_id)},{"$set" : {"status" : "rented"}})
            return True
        except:
            return False

    def revoke(self, car_id):
        conn = init()
        db = conn.innovaccer
        coll = db.cars
        try:
            coll.car_info.update({"_id" : ObjectId(car_id)},{"$set" : {"status" : ""}})
            return True
        except:
            return False

    def fetch_rent(self, car_id):
        conn = init()
        db = conn.innovaccer
        coll = db.cars
        try:
            result = coll.car_rent.find_one({"_id" : ObjectId(car_id)})
            return result
        except:
            return False

    def cal_sale_prof(self):
        conn = init()
        db = conn.innovaccer
        coll = db.cars
        try:
            result = coll.car_info.aggregate([{'$group' : {'_id' : None, 'sale' : {'$sum' : '$selling_price'}}}])
            print [result for result in result]
            return True
        except:
            return False
        
