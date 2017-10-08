from flask import jsonify, g
import os
import config
import time

TEST_ENV = getattr(config, 'TEST_ENV', False)

def respond(response, http_status=200):
    
    if TEST_ENV:
        response['environment'] = 'testing'

    if 'http_status' in response:
        http_status = response['http_status']
        del response['http_status']

    return jsonify(response), http_status

get_timestamp = lambda: int(time.time() * 1000)

def getList(string):
    slist=string.split(',')
    return slist