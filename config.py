import os


PASSWORD = os.environ.get('PASSWORD')

class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{}@localhost/test1'.format(PASSWORD)
    SECRET_KEY = 'some_secret_key'

    ### Flask Security ###
    SECURITY_PASSWORD_SALT = 'noprszdfdkrjtmybyohh'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
