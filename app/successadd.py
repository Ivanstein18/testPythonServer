import psycopg2


def addExpended(expended):

    with psycopg2.connect(dbname="xpeH", user="postgres", password= "1234", host= "127.0.0.1") as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE registerUsers(userName text, hash text);")


            
            conn.commit()