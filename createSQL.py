import psycopg2
from app.general import connect_database_create


conn = connect_database_create()
with conn.cursor() as cur:
    cur.execute("CREATE TABLE registerUsers(userName text, hash text, expenses text);")
    conn.commit()
    
    

        
