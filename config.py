class config:
    db = {
        'user'     : 'newuser',
        'password' : '0000',
        'host'     : '127.0.0.1',
        'port'     : '3306',
        'database' : 'rest_api'
    }


    DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8" 
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev'