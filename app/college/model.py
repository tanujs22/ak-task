import config
import json, datetime
from datetime import datetime
import time

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

    