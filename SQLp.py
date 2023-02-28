import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE IF EXISTS Phone;
        DROP TABLE IF EXISTS Client;
        """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Client(
                client_id SERIAL PRIMARY KEY,
                name VARCHAR(60) NOT NULL,
                surname VARCHAR(60) NOT NULL,
                e_mail VARCHAR(60) NOT NULL UNIQUE);
                """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Phone(
                number DECIMAL UNIQUE CHECK(number <= 99999999999),
                client_id INTEGER REFERENCES Client(client_id));
                """)
        conn.commit()


def add_client(conn, name, surname, e_mail, phones=None):
    cur.execute("""
            INSERT INTO Client(name, surname, e_mail)
            VALUES(%s, %s, %s)
            RETURNING client_id, name, surname, e_mail;
            """, (name, surname, e_mail))
    conn.commit()

def add_phone(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO Phone(number, client_id)
                VALUES(number, client_id)
                RETURNING client_id, name, surname, e_mail
                """), (client_id, number)
    print(cur.fetchone())

def change_client(conn, client_id, name=None, surname=None, e_mail=None, number=None):
    conn.execute("""
        UPDATE Client
        SET name=%s, surname=%s, e_mail=%s
        WHERE client_id=%s
        RETURNING client_id, name, surname, e_mail;
        """, (name, surname, e_mail, client_id))

    conn.execute("""
        UPDATE Phone
        SET number=%s
        WHERE client_id=%s
        RETURNING client_id, number;
        """, (number, client_id))

def delete_phone(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM Phone
                WHERE client_id=%s;
                """, (client_id,))
    print(cur.fetchall())

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM Client
            WHERE client_id=%s;
            """, (client_id,))
    print(cur.fetchall())

def find_client(cur, name=None, surname=None, e_mail=None, number=None):
    cur.execute("""
        SELECT c.name, c.surname, c.e_mail, p.number FROM Client AS c
        LEFT JOIN Phone AS p ON c.client_id = p.client_id
        WHERE c.name=%s OR c.surname=%s OR c.e_mail=%s OR p.number=%s;
        """, (name, surname, e_mail, number))
    return cur.fetchall()



with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        print(create_db(conn))
        print(add_client(conn, 'Murz', 'Bulkin', 'murz@mail.ru', '89999999999'))
        print(add_phone(conn, '1', '899999999999'))
        print(change_client(conn, '1', 'Kuzya', 'Murzikov', 'kuziaa@mail.ru', '89999999998'))
        print(delete_phone(conn, '1', '89999999998'))
        print(delete_client(conn, '1'))
        print(find_client(conn, 'Murz'))

    conn.close()

