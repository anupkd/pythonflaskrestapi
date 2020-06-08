from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })

class BotDto:
    api = Namespace('bot', description='bot related operations')
    bot = api.model('bot', {
        'reply': fields.String(required=True, description='response') 
    })


class EmployeeDto:
    api = Namespace('employee', description='employee related operations')
    employee = api.model('employee', {
        'email': fields.String(required=True, description='employee email address'),
        'fname': fields.String(required=True, description='employee fname'),
        'lname': fields.String(required=False, description='employee lname'),
        'phone_no': fields.String(description='Phone no'),
        'empno': fields.String(description='Employee no'),
        'isactive': fields.String(description='active/in active')
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })