import uuid
import datetime
import cx_Oracle
from app.main import db
from app.main.model.user import User
import json
from ..config import  ORACLE_DB_PATH,TWILIO_SID ,TWILIO_TOKEN ,WHATSAPP_SENDER_NO
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

class Messagerespo:
  def __init__(self, intent, message):
    self.intent = intent
    self.message = message


def upd_user_session(phone_no,message,body):
    con = cx_Oracle.connect(ORACLE_DB_PATH)
    cur = con.cursor()
    #cur.execute("select sor_order_no, cst_code , cst_name  from om.om_sales_order s inner join cm.cm_customer c on c.cst_Seq = s.cst_seq    where  ort_Seq = 2 and  SOR_DELIVERED_STATUS  in ('C','BR') and Loc_Seq in (select loc_seq from am.am_location where    attribute4 ='Y')")
    #cur.execute("select 'uname' username,'333' phone_no ,'ddd@ff.com' email  from dual")
    outVal = cur.var(str)
    outVal2 = cur.var(str)
    outSessionid = cur.var(str)
    outLastIntent = cur.var(str)
    outLastReply = cur.var(str)
    con.outputtypehandler = OutputTypeHandler
    cur.callproc('USP_EMP_UPD_SESSION', [phone_no, message , outVal,outVal2,outSessionid,outLastIntent,outLastReply ])
    #cur.rowfactory = lambda *args: dict(zip([d[0].lower() for d in cur.description], args))
    print (outLastReply.getvalue())
    #rslt = cur.fetchall()
    sessionid= outSessionid.getvalue()
    answer = processmessage(outLastIntent.getvalue(),body,outLastReply.getvalue() )
    sendmessage( phone_no,answer.message)   
    upd_reply_session(con,phone_no,sessionid,answer.intent,answer)
    con.commit()
    cur.close()
    con.close()
    return    '{"status_code":"'+outVal.getvalue()+'","status_name":"'+  outVal2.getvalue() + '","sessionid":"'+  outSessionid.getvalue() + '"}'

def upd_reply_session(con,phone_no,sessionid,reply_intent,message):
    cur = con.cursor()
    #cur.execute("select sor_order_no, cst_code , cst_name  from om.om_sales_order s inner join cm.cm_customer c on c.cst_Seq = s.cst_seq    where  ort_Seq = 2 and  SOR_DELIVERED_STATUS  in ('C','BR') and Loc_Seq in (select loc_seq from am.am_location where    attribute4 ='Y')")
    cur.execute("update tmp_empl_sessions set last_reply ='{}' ,last_reply_object ='{}' where sessionid={}".format(reply_intent,message,sessionid) )
    cur.close()
    return    'Success' 

def sendmessage(whatsappno,messages):
      account_sid = TWILIO_SID 
      auth_token = TWILIO_TOKEN
      client = Client(account_sid, auth_token)
      message = client.messages \
           .create(
             #media_url=['http://www.africau.edu/images/default/sample.pdf'],
             from_=WHATSAPP_SENDER_NO,
             body=messages,
             to='whatsapp:+' + whatsappno
           )        
      return 'Send'

def greetings(mess):
    return Messagerespo('homemenuselected',"selected {}".format(mess ))
 
def homemenuselected(mess):
    return Messagerespo('goodbye',"Your answer {}".format('1')) 

def welcome(mess):
    return Messagerespo('greetings',"Welcome to HRMS bot.\n 1.Leave \n 2.Salary" )

def goodbye(mess):
    return Messagerespo('greetings',"Welcome to HRMS bot.\n 1.Leave \n 2.Salary" )

def processmessage(lastintent,inmess,lastreply ):
    resp=""
    print(lastintent)
    if(inmess.lower().find('bye') >= 0):
       return Messagerespo('goodbye',"Thanks for using our service.See you again")
 
    switcher = {
        'greetings': greetings,
        'homemenuselected': homemenuselected,
        '' : welcome,
        None : welcome,
        'goodbye' : goodbye    
    }
    func = switcher[lastintent](inmess)  
    return func;

def OutputTypeHandler(cursor, name, defaultType, size, precision, scale):
    if defaultType == cx_Oracle.CLOB:
        return cursor.var(cx_Oracle.LONG_STRING, arraysize = cursor.arraysize)
    elif defaultType == cx_Oracle.BLOB:
        return cursor.var(cx_Oracle.LONG_BINARY, arraysize = cursor.arraysize)