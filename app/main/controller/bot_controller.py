from flask import request, jsonify
from flask_restplus import Resource

from app.main.service.auth_helper import Auth
from ..util.dto import BotDto
from twilio.twiml.messaging_response import MessagingResponse
from ..config import TWILIO_SID ,TWILIO_TOKEN ,WHATSAPP_SENDER_NO
from twilio.rest import Client
from ..service.bot_service import   upd_user_session,upd_reply_session
from werkzeug.datastructures import ImmutableMultiDict
import json

api = BotDto.api
bot_reply = BotDto.bot

#https://channels.autopilot.twilio.com/v1/ACde03e16509b548e3311e4f8744ed20bd/UAb81023443432317a52e01612f3913800/twilio-messaging/whatsapp

@api.route('/test')
class test(Resource):
    def post(self):
        data = request.get_json(silent=True)
        print(data)
        reply = {
            "fulfillmentText": "Reply from api",
        }
        return jsonify(reply)

@api.route('/chat')
class ProcessChat(Resource):
    """
        Chat Resource
    """
    @api.doc('process chat')
    #@api.expect(user_auth, validate=True)
    def post(self):
        phoneno = str.replace(request.values.get(f'From'), 'whatsapp:+','')
        # get the post data
        post_data = request.values
        print(post_data)
        imd = ImmutableMultiDict(post_data)
        post_data=json.dumps(imd.to_dict(flat=False))
        rslt = json.loads(upd_user_session(phoneno,post_data,request.values.get(f'Body')))
        print(rslt['sessionid'])
        return 'Success'

