import psycopg2


def includingUsernameAndPasswordInBase(username, password):





    with psycopg2.connect(dbname="xpeh", user="postgres", password= "1234", host= "127.0.0.1") as conn:

        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO registerUsers (userName, hash) VALUES ('{username}', '{password}');")
            conn.commit()