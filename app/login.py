import psycopg2


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
                if hash != password:
                    return "пароль не верный"
                return "OK"