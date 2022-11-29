from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response
import psycopg2
from app.login import *
from app.registration import *
from app.general import *




app = FastAPI()

@app.get("/")
def index(usernameS= Cookie(default=None)):
    with open("templates/index.html", "r") as f:
        index_page = f.read()
    if usernameS:
        if check_valid_sign_data(usernameS):
            username = username_from_usernameS(usernameS)
            with open("templates/login.html", "r") as f:
                login_page = f.read().format(username)
            return Response(login_page, media_type= "text/html")
        else:
            respons = Response(index_page, media_type= "text/html")
            return respons.delete_cookie(key= "usernameS")
    else:        
        return Response(index_page, media_type= "text/html")


@app.post("/login")
def login(username= Form(...), password= Form(...)):
    if checkingUsernameAndPassword(username, password) == "user не найден":
        return Response("User не найден", media_type= "text/html")
    elif checkingUsernameAndPassword(username, password) == "пароль не верный":
        return Response("Пароль не верный", media_type= "text/html")
    else:
        with open("templates/login.html", "r") as f:
            login_page = f.read().format(username)
        response = Response(login_page, media_type= "text/html")
        response.set_cookie(key= 'usernameS', value= sign_cookie(username))
        return response

@app.get("/registretion")
def registretion():
    with open("templates/registretion.html", "r") as f:
        registretion_page = f.read()
    return Response(registretion_page, media_type= "text/html")


@app.post("/completereg")
def completeReg(username= Form(...), password= Form(...)):
    includingUsernameAndPasswordInBase(username, password)

    with open("templates/successful_reg.html", "r") as f:
        congretulationsPage = f.read()
    return Response(congretulationsPage, media_type= "text/html")


@app.post("/successAdd")
def successAdd(expenses= Form(...)):
    return Response(f"{expenses}", media_type= "text/html")

    
