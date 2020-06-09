import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']
oracle_db_path =os.getenv('DATABASE_URL', '') 
#os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    ORACLE_DB_URL =  os.getenv('DATABASE_URL', '')
    account_sid =   os.getenv('account_id','ACde03e16509b548e3311e4f8744ed20bd')
    auth_token =   os.getenv('auth_token','b17e89486a7540857d0b573304273f7f') 
    WHATSAPP_SENDER_NO = ''
    RABBITMQ_URL = 'localhost'

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Config.ORACLE_DB_URL = 'intf/intf2018@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=ec2-34-247-167-181.eu-west-1.compute.amazonaws.com)(PORT=1521)))(CONNECT_DATA=(SID=axiomstg)))'
    print('Dev')

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Config.ORACLE_DB_URL = 'intf/intf2018@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=ec2-34-247-167-181.eu-west-1.compute.amazonaws.com)(PORT=1521)))(CONNECT_DATA=(SID=axiomstg)))'
    print('Test')


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    Config.ORACLE_DB_URL = oracle_db_path
    print('Production')

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
ORACLE_DB_PATH = Config.ORACLE_DB_URL
TWILIO_SID = Config.account_sid
TWILIO_TOKEN = Config.auth_token
WHATSAPP_SENDER_NO='whatsapp:+14155238886'
RABBITMQ_URL = Config.RABBITMQ_URL