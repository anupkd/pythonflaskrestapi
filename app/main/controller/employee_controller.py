from flask import request
from flask_restplus import Resource

from ..util.dto import EmployeeDto,UserDto
#from ..service.user_service import save_new_user, get_all_users, get_a_user
from ..service.employee_service import   get_all_employees, get_a_employee
from app.main.service.auth_helper import Auth

api = EmployeeDto.api
_user = EmployeeDto.employee


@api.route('/')
class EmployeeList(Resource):
    @api.doc('list_of_registered_employees')
    @api.marshal_list_with(_user, envelope='data')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    def get(self):
        """List all registered employees"""
        # get auth token
        #rsp = Auth.get_logged_in_user(request)
        #if(rsp[1] != 200):
        #   return rsp 
        return get_all_employees()


@api.route('/validate/<phone_no>')
@api.param('phone_no', 'The User Mobile No')
@api.response(404, 'User not found.')
class Employee(Resource):
    @api.doc('get a Employee')
    @api.marshal_with(_user)
    def get(self, phone_no):
        """get a employee given its phone no"""
        user = get_a_employee(phone_no)
        if not user:
            api.abort(404)
        else:
            return user