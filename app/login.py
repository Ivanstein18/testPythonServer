import psycopg2
import hmac
from .general import hashing_password, connect_database_create


def verify_password(password, hash):
    hashingPassword = hashing_password(password)
    return hmac.compare_digest(hash, hashingPassword)

def checkingUsernameAndPassword(username, password):
    conn = connect_database_create()
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