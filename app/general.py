from .secret_const import SECRET_KEY, PASSWORD_SALT
from app.customization_const import DBNAME, DBUSER, DBPASSWORD, DBHOST
from fastapi.responses import Response
from fastapi import Form, Cookie
import hmac, hashlib, base64, psycopg2


def sign_data(data):
    sign_data = hmac.new(key= SECRET_KEY.encode(), msg= data.encode(), digestmod= hashlib.sha256).hexdigest().upper()
    return sign_data

def data_b64_encode(data):
    code = (base64.b64encode(data.encode())).decode()
    return code

def data_b64_decode(data_b64_encode):
    decode = (base64.b64decode(data_b64_encode.encode())).decode()
    return decode

def check_valid_sign_data(usernameS):
    usernameB64, sign = usernameS.split(".")
    username = data_b64_decode(usernameB64)
    check = hmac.compare_digest(sign, sign_data(username))
    if check:
        return True
    else:
        return False

def get_username_from_usernameS(usernameS):
    usernameB64, sign = usernameS.split(".")
    username = data_b64_decode(usernameB64)
    return username

def sign_cookie(username):
    sign_cookie = f"{data_b64_encode(username)}.{sign_data(username)}"
    return sign_cookie


def hashing_password(password, salt= PASSWORD_SALT):
    hashing_password = hashlib.sha256((f'{password}+{salt}').encode()).hexdigest()
    return hashing_password


def decorate_with_Form_Cookie(func):
    def wrapper(expenses= Form(default= "undefined"), usernameS= Cookie(default=None)): 
        if usernameS:        
            if check_valid_sign_data(usernameS):
                res = func(expenses, usernameS)
        else:
            with open("templates/index.html", "r") as f:
                index_page = f.read()
            return Response(index_page, media_type= "text/html")
        return res
    return wrapper

def decorate_with_Cookie(func):
    def wrapper(usernameS= Cookie(default=None)): 
        if usernameS:        
            if check_valid_sign_data(usernameS):
                res = func(usernameS)
        else:
            with open("templates/index.html", "r") as f:
                index_page = f.read()
            return Response(index_page, media_type= "text/html")
        return res
    return wrapper


def connect_database_create(dbname= DBNAME, user= DBUSER, password= DBPASSWORD, host= DBHOST):
    try:
        with psycopg2.connect(dbname= dbname, user= user, password= password, host= host) as conn:
            return conn
    except Exception as e:
        print(str(e))
        with open("templates/oops.html", "r") as f:
            oops_page = f.read()
        return Response(oops_page, media_type= "text/html")