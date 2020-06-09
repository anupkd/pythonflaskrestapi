import uuid
import datetime
import cx_Oracle
from app.main import db
from app.main.model.user import User
import json
from ..config import  ORACLE_DB_PATH,TWILIO_SID ,TWILIO_TOKEN ,WHATSAPP_SENDER_NO
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from app.main.util.quemanage import publismessage
from json import JSONEncoder

class Messagerespo:
  def __init__(self, intent, message,menu,args):
    self.intent = intent
    self.message = message
    self.menu = menu
    self.vars = args

class MessageCollection:
  def __init__(self, option, args):
    self.option = option
    self.args = args
  
  def toJSON(self):
      '''
      Serialize the object custom object
      '''
      return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class QMess:
  def __init__(self, phoneno, data,module):
    self.phoneno = phoneno
    self.data = data
    self.module = module

  def toJSON(self):
      '''
      Serialize the object custom object
      '''
      return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
 
# subclass JSONEncoder
class MessageEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

def upd_user_session(phone_no,message,body):
    con = cx_Oracle.connect(ORACLE_DB_PATH)
    cur = con.cursor()
    #cur.execute("select sor_order_no, cst_code , cst_name  from om.om_sales_order s inner join cm.cm_customer c on c.cst_Seq = s.cst_seq    where  ort_Seq = 2 and  SOR_DELIVERED_STATUS  in ('C','BR') and Loc_Seq in (select loc_seq from am.am_location where    attribute4 ='Y')")
    #cur.execute("select 'uname' username,'333' phone_no ,'ddd@ff.com' email  from dual")
    outVal = cur.var(str)
    outVal2 = cur.var(str)
    outSessionid = cur.var(str)
    outLastIntent = cur.var(str)
    outLastReply = cur.var(cx_Oracle.CLOB)
    #cur.setinputsizes(outLastReply = cx_Oracle.CLOB)
    #cur.setinputsizes(outVal =  cx_Oracle.STRING,outVal2 =  cx_Oracle.STRING)
    con.outputtypehandler = OutputTypeHandler
    
    cur.callproc('USP_EMP_UPD_SESSION', [phone_no, message , outVal,outVal2,outSessionid,outLastIntent,outLastReply ])
    #cur.rowfactory = lambda *args: dict(zip([d[0].lower() for d in cur.description], args))
    print(outLastReply.getvalue())
    if(outLastReply.getvalue() != None):
       print('1')
       lreply =   str(outLastReply.getvalue())
    else:
       print(2) 
       lreply = MessageEncoder().encode(Messagerespo('','','',[]))
    #rslt = cur.fetchall()
    sessionid= outSessionid.getvalue()
    answer = processmessage(phone_no,outLastIntent.getvalue(),body,json.loads(lreply) )
    sendmessage( phone_no,answer.message) 
    print(answer)  
    upd_reply_session(con,phone_no,sessionid,answer.intent,MessageEncoder().encode(answer))
    con.commit()
    cur.close()
    con.close()
    return    '{"status_code":"'+outVal.getvalue()+'","status_name":"'+  outVal2.getvalue() + '","sessionid":"'+  outSessionid.getvalue() + '"}'

def upd_reply_session(con,phone_no,sessionid,reply_intent,message):
    cur = con.cursor()
    #cur.execute("select sor_order_no, cst_code , cst_name  from om.om_sales_order s inner join cm.cm_customer c on c.cst_Seq = s.cst_seq    where  ort_Seq = 2 and  SOR_DELIVERED_STATUS  in ('C','BR') and Loc_Seq in (select loc_seq from am.am_location where    attribute4 ='Y')")
    print(message)
    print(reply_intent)
    outVal = cur.var(str)
    con.outputtypehandler = OutputTypeHandler
    cur.callproc('USP_EMP_REPLY_UPDATE', [reply_intent, message , sessionid,outVal ])
    #cur.execute("update tmp_empl_sessions set last_reply ='{}' ,last_reply_object ='{}' where sessionid={}".format(reply_intent,message,sessionid) )
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

def greetings(mess,lastreply):
    l=['1','2','3','4','5']
    if (l.__contains__(mess)==False):
        return Messagerespo('greetings',"Sorry ,i didn't get you.Please try again",lastreply['menu'],lastreply['vars'])
    switcher = {
        '1': payslip,
        '2': vacation,
        '3' : exitrequest,
        '4' : travelrequest,
        '5' : exitmessage    
    }
    switcher2 = {
        '1': 'payslip',
        '2': 'vacation',
        '3' : 'exitrequest',
        '4' : 'travelrequest',
        '5' : 'exitmessage'    
    }    
    func = switcher[mess]('')  
    sessionObj  = lastreply['vars']
    sessionObj.append(["home_menu_selected",mess])
    print (switcher2[mess])
    return Messagerespo('homemenuselected',func,switcher2[mess],sessionObj)

#home menu functions
def exitmessage(args):
    return  "Thanks for using our service.See you again"   

def payslip(args):
    return  "Select an option.\n1.Latest Payslip details \n2.Download Payslip \n3.Back"   

def vacation(args):
    return  "Select an option.\n1.Leave Balance \n2.Leave Request \n3.Leave status \n4.Duty Resumption \n5.Leave Approval  \n6.Back" 

def exitrequest(args):
    return  "Select an option.\n1.Exit Request \n2.Entry Request \n3.Request status \n4.Request Approval  \n5.Back" 

def travelrequest(args):
    return  "Select an option.\n1.Travel Request \n2.Ticket Request \n3.Request status \n4.Request Approval  \n5.Back" 

#bot status functions 
def homemenuselected(mess,lreply):
    sessionObj  = lreply['vars']
    if(lreply['menu'] == 'payslip' and mess == "2" ):
        sessionObj.append(["submenu_selected",mess] )
        return Messagerespo('payslipdownload',"Enter the month and year in the format (MM-YYYY).Eg 12-2020",'payslip',sessionObj)
    #publismessage('payslip','payslip_pdf_request',mess)
    sessionObj.append(["submenu_selected",mess] )
    print(sessionObj)
    return Messagerespo('goodbye',"Your answer {}".format(mess),'payslip',sessionObj) 

def payslipdownload(mess,lreply):
    sessionObj  = lreply['vars']
    phoneno = get_data( sessionObj,"phoneno")
    publismessage('payslip','payslip_pdf_request', QMess(phoneno=phoneno,data=mess,module='payslip-pdf').toJSON())
    return Messagerespo('goodbye',"Your file will be send in a while .." ,'payslip',sessionObj) 

def welcome(mess,lreply):
    #publismessage('payslip','payslip_pdf_request',mess)
    return Messagerespo('greetings',"Welcome to HRMS bot.\n1.Payslip \n2.Vacation \n3.Exit/Entry Request \n4.Travel Request \n5.Exit","",[] )

def goodbye(mess,lreply):
    return Messagerespo('greetings',"Welcome to HRMS bot.\n1.Payslip \n2.Vacation \n3.Exit/Entry Request \n4.Travel Request \n5.Exit","",[] )

def processmessage(phone_no,lastintent,inmess,lastreply ):
    resp=""
    print(lastintent)
    if (get_data( lastreply["vars"],"phoneno") == ""):
        lastreply["vars"].append(["phoneno",phone_no])   
    if(inmess.lower().find('bye') >= 0):
       return Messagerespo('goodbye',"Thanks for using our service.See you again",lastreply['menu'],lastreply['vars'])
 
    switcher = {
        'greetings': greetings,
        'homemenuselected': homemenuselected,
        '' : welcome,
        None : welcome,
        'goodbye' : goodbye, 
	'payslipdownload':payslipdownload   
    }
    func = switcher[lastintent](inmess,lastreply)  
    return func;

def get_data(data,param):
    '''
    Convert string array to json array
    '''
    result = []
    for item in data:
        if(item[0]== param):
           return(item[1])
    return ""

def OutputTypeHandler(cursor, name, defaultType, size, precision, scale):
    if defaultType == cx_Oracle.CLOB:
        return cursor.var(cx_Oracle.LONG_STRING, arraysize = cursor.arraysize)
    elif defaultType == cx_Oracle.BLOB:
        return cursor.var(cx_Oracle.LONG_BINARY, arraysize = cursor.arraysize)