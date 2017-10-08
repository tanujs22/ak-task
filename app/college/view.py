from model import College

def list_college(parameters):
    response = {"data": [], "status": "failed"}
    return response

def add_college(parameters):
    response = {"message": [], "status": "failed"}
    csvfile = parameters['csvfile']
    cl = College()
    result = cl.save_college(csvfile)
    if result:
        result = 'created!'
    response['data'] = result
    return response
    