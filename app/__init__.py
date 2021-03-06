# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.employee_controller import api as employee_ns
from .main.controller.bot_controller import api as bot_ns


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Rest Api for Whatsapp Bot',
          version='1.0',
          description='Whatsapp bot Webhook restplus web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(employee_ns, path='/employee')
api.add_namespace(bot_ns, path='/bot')
