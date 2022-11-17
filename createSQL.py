import psycopg2

with psycopg2.connect(dbname="xpeH", user="postgres", password= "1234", host= "127.0.0.1") as conn:


    with conn.cursor() as cur:

        # cur.execute("CREATE TABLE registerUsers(userName text, hash text);")
        # conn.commit()

        # cur.execute("INSERT INTO registerUsers (userName, hash) VALUES ('ivanstein', '1234');")
        # conn.commit()

        cur.execute("SELECT userName FROM registerUsers;")
        name = cur.fetchone()[0]
        cur.execute(f"SELECT hash FROM registerUsers WHERE username = '{name}';")
        print(cur.fetchone()[0])

        
