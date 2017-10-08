from model import College

def list_college(parameters):
    response = {"data": [], "status": "failed"}
    university = parameters.get('university', '')
    city = parameters.get('city', '')
    fees = parameters.get('fees', '')
    marks = parameters.get('marks', '')
    if university:
        university = university.split(',')
    if city:
        city = city.split(',')
    cl = College()
    result = cl.fetch_all(university, city, fees, marks)
    response['data'] = result
    return response

def add_college(parameters):
    response = {"message": [], "status": "failed"}
    csvfile = parameters['csvfile']
    cl = College()
    result = cl.save_college(csvfile)
    if result:
        result = 'created!'
    response['message'] = result
    response['status'] = 'success'
    return response
    