import os

class Config:
    SECRET_KEY = os.urandom(24)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'your_mysql_username'
    MYSQL_PASSWORD = 'your_mysql_password'
    MYSQL_DB = 'flask_notepad'
    MYSQL_CURSORCLASS = 'DictCursor'
