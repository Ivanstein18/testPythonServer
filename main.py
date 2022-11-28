from fastapi import FastAPI
from fastapi.responses import Response
from fastapi import Form
from fastapi import Body
import psycopg2
from app.login import *
from app.registration import *



app = FastAPI()

@app.get("/")
def index():
    with open("templates/index.html", "r") as f:
        index_page = f.read()
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
            return response.set_cookie(key= 'username', value= username)

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

    
