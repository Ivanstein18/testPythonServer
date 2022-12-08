import psycopg2
from .general import hashing_password, connect_database_create


def includingUsernameAndPasswordInBase(username, password):
    conn = connect_database_create()
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO registerUsers (userName, hash) VALUES ('{username}', '{hashing_password(password)}');")
        conn.commit()