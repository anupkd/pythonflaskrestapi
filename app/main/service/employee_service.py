import uuid
import datetime
import cx_Oracle
from app.main import db
from app.main.model.user import User
import json
from ..config import  ORACLE_DB_PATH

def get_all_employees():
    #print(ORACLE_DB_PATH)
    con = cx_Oracle.connect( ORACLE_DB_PATH)
    #'intf/intf2018@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=axiom-db.cffm1swmuki3.eu-west-1.rds.amazonaws.com)(PORT=1521)))(CONNECT_DATA=(SID=AXIOM)))')
    cur = con.cursor()
    #cur.execute("select sor_order_no, cst_code , cst_name  from om.om_sales_order s inner join cm.cm_customer c on c.cst_Seq = s.cst_seq    where  ort_Seq = 2 and  SOR_DELIVERED_STATUS  in ('C','BR') and Loc_Seq in (select loc_seq from am.am_location where    attribute4 ='Y')")
    cur.execute("select *  from tmp_emp_Dets")
    cur.rowfactory = lambda *args: dict(zip([d[0].lower() for d in cur.description], args))
    rslt = cur.fetchall()
    print (rslt)
    cur.close()
    return rslt #( [dict(ix) for ix in rslt] )


def get_a_employee(phone_no):
    con = cx_Oracle.connect(ORACLE_DB_PATH)
    cur = con.cursor()
    #cur.execute("select sor_order_no, cst_code , cst_name  from om.om_sales_order s inner join cm.cm_customer c on c.cst_Seq = s.cst_seq    where  ort_Seq = 2 and  SOR_DELIVERED_STATUS  in ('C','BR') and Loc_Seq in (select loc_seq from am.am_location where    attribute4 ='Y')")
    #cur.execute("select 'uname' username,'333' phone_no ,'ddd@ff.com' email  from dual")
    outVal = cur.var(str)
    outVal2 = cur.var(str)
    cur.callproc('USP_EMP_UPD_SESSION', [phone_no,'test' , outVal,outVal2])
    #cur.rowfactory = lambda *args: dict(zip([d[0].lower() for d in cur.description], args))
    print (outVal.getvalue())
    #rslt = cur.fetchall()
    #cur.close()
    return     'Success' 

