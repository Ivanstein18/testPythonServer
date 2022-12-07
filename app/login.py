import psycopg2
import hmac
from .general import hashing_password


def verify_password(password, hash):
    hashingPassword = hashing_password(password)
    return hmac.compare_digest(hash, hashingPassword)

def checkingUsernameAndPassword(username, password):
    with psycopg2.connect(dbname="xpeH", user="postgres", password= "1234", host= "127.0.0.1") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"SELECT userName FROM registerUsers WHERE userName = '{username}';")
                name = cur.fetchone()[0]                
            except(TypeError):
                return "user не найден"
            cur.execute(f"SELECT hash FROM registerUsers WHERE username = '{name}';")
            hash = cur.fetchone()[0]            
            if not verify_password(password, hash= hash):
                return "пароль не верный"
            return "OK"