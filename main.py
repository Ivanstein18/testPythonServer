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
            username = get_username_from_usernameS(usernameS)
            with open("templates/login.html", "r") as f:
                login_page = f.read().format(username)
            return Response(login_page, media_type= "text/html")
        else:
            respons = Response(index_page, media_type= "text/html")
            return respons.delete_cookie(key= "usernameS")
    else:        
        return Response(index_page, media_type= "text/html")


@app.post("/login")
def login(username= Form(default= "undefined"), password= Form(default= "undefined")):
    if (username or password) == "undefined":
        return Response("Вы оставили поле пустым", media_type= "text/html")
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
def completeReg(username= Form(default= "undefined"), password= Form(default= "undefined")):
    if (username or password) == "undefined":
        return Response("Вы оставили поле пустым", media_type= "text/html")
    else:
        includingUsernameAndPasswordInBase(username, password)
        with open("templates/successful_reg.html", "r") as f:
            congretulationsPage = f.read()
        return Response(congretulationsPage, media_type= "text/html")


@app.post("/successAdd")
@decorate_with_Form_Cookie
def successAdd(expenses= Form(default= "undefined"), usernameS= Cookie(default=None)):
    if expenses == "undefined":
        return Response("Вы оставили поле пустым", media_type= "text/html")
    username = get_username_from_usernameS(usernameS)
    try:
        conn = connect_database_create()
        with conn.cursor() as cur:
            cur.execute(f"SELECT expenses FROM registerusers WHERE username='{username}';")
            user_expenses = cur.fetchone()[0]
            if not user_expenses:
                cur.execute(f"UPDATE registerusers SET expenses='{expenses}' WHERE username='{username}';")
            else:
                cur.execute(f"UPDATE registerusers SET expenses='{str(int(user_expenses) + int(expenses))}' WHERE username='{username}';")
            conn.commit()
        with open("templates/successful_add.html", "r") as f:
            successful_add_page = f.read()
        return Response(successful_add_page, media_type= "text/html")
    except Exception as e:
        print(str(e))
        with open("templates/oops.html", "r") as f:
            oops_page = f.read()
        return Response(oops_page, media_type= "text/html")


@app.get("/conclusion")
@decorate_with_Cookie
def conclusion(usernameS= Cookie(default=None)):
    username = get_username_from_usernameS(usernameS)
    try:
        conn = connect_database_create()
        with conn.cursor() as cur:
            cur.execute(f"SELECT expenses FROM registerusers WHERE username='{username}';")
            user_expenses = cur.fetchone()[0]
            if not user_expenses:
                user_expenses == 0
        with open("templates/conclusion.html", "r") as f:
            conclusion_page = f.read().format(username, user_expenses)
        return Response(conclusion_page, media_type= "text/html")
    except Exception as e:
        print(str(e))
        with open("templates/oops.html", "r") as f:
            oops_page = f.read()
        return Response(oops_page, media_type= "text/html")


@app.get("/nullify")
@decorate_with_Cookie
def nullify(usernameS= Cookie(default=None)):
    username = get_username_from_usernameS(usernameS)
    try:
        conn = connect_database_create()
        with conn.cursor() as cur:
            cur.execute(f"UPDATE registerusers SET expenses='0' WHERE username='{username}';")
        conn.commit()
        with open("templates/nullify.html", "r") as f:
            nullify_page = f.read()
        response = Response(nullify_page, media_type= "text/html")
        return response
    except Exception as e:
        print(str(e))
        with open("templates/oops.html", "r") as f:
            oops_page = f.read()
        return Response(oops_page, media_type= "text/html")




    