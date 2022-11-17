from fastapi import FastAPI
from fastapi.responses import Response
from fastapi import Form
from fastapi import Body
import psycopg2




app = FastAPI()

@app.get("/")
def index():
    with open("templates/index.html", "r") as f:
        index_page = f.read()
    return Response(index_page, media_type= "text/html")



@app.post("/login")
def login(username= Form(...), password= Form(...)):
    with psycopg2.connect(dbname="xpeH", user="postgres", password= "1234", host= "127.0.0.1") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"SELECT userName FROM registerUsers WHERE userName = '{username}';")
                name = cur.fetchone()[0]                
            except(TypeError):
                return Response("Пользователь не найден", media_type= "text/html")     #???????????????????user не найден
          
            cur.execute(f"SELECT hash FROM registerUsers WHERE username = '{name}';")
            hash = cur.fetchone()[0]            
            if hash != password:
                return Response("Неверный пароль!", media_type= "text/html")     #???????????????????пароль не верный
        
    with open("templates/login.html", "r") as f:
        login_page = f.read().format(username, password)
    return Response(login_page, media_type= "text/html")
