import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig(object):

    # database config
    HOST = str(os.environ.get('DB_HOST'))
    USER = str(os.environ.get('DB_USERNAME'))
    PASSWORD = str(os.environ.get('DB_PASSWORD'))
    DATABASE = str(os.environ.get('DB_DATABASE'))

    # jwt config
    JWT_SECRET_KEY = str(os.environ.get('FLASK_JWT_SECRET_KEY'))

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + USER + ":" + PASSWORD + "@" + HOST + "/" + DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True