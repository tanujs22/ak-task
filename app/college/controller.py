from flask import Blueprint, request
from werkzeug.datastructures import CombinedMultiDict, MultiDict
from tools.CORS import crossdomain
from tools.Toolkit import respond
from view import add_college

college_api = Blueprint('college', __name__, url_prefix='/college')

@college_api.route('/', methods=['GET'])
@crossdomain(origin='*')
def get_college():
	parameters = CombinedMultiDict([request.args, request.form])
	response = list_college(parameters)
	return respond(response)

@college_api.route('/add', methods=['POST'])
@crossdomain(origin='*')
def save_college():
	parameters = request.get_json()
	response = add_college(parameters)
	return respond(response)
