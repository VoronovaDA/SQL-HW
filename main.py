import psycopg2


with psycopg2.connect(database="homework_db", user="postgres", password="7404") as conn:
    with conn.cursor() as cur:
        cur.execute("""
                    DROP TABLE Phones;
                    DROP TABLE Client;
                    """)


    def create_db(cur):
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Client(
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(60) NOT NULL,
                last_name VARCHAR(60) NOT NULL,
                email VARCHAR(60) NOT NULL UNIQUE);
                        """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Phones(
                phone_id SERIAL PRIMARY KEY,
                phone VARCHAR(20),
                client_id INTEGER REFERENCES Client(client_id) ON DELETE CASCADE);
                        """)
            print("Таблица/цы успешно создана/ны!")
            conn.commit()

                
    def add_client(cur, first_name, last_name, email):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Client(first_name, last_name, email)
                VALUES(%s, %s, %s)
                RETURNING client_id, first_name, last_name, email;
                """, (first_name, last_name, email, ))            
            print("Запись успешно добавлена ​​в таблицу!")
            print(cur.fetchone())
            return cur.fetchone()
            
        
    def add_phone(cur, client_id, phone):
        with conn.cursor() as cur:           
            cur.execute("""
                INSERT INTO Phones(client_id, phone)
                VALUES(%s, %s)
                RETURNING client_id, phone;
                """, (client_id, phone, ))         
            print( "Запись успешно добавлена ​​в таблицу!")
            print(cur.fetchone())
            return cur.fetchone()

        
    def change_client(cur, first_name, last_name, client_id):
        with conn.cursor() as cur:          
            cur.execute("""
                UPDATE Client
                SET first_name=%s , last_name=%s  
                WHERE client_id=%s
                RETURNING client_id, first_name, last_name, email;
                """, (first_name, last_name, client_id, ))           
            print("Записи обновлены!")
            print(cur.fetchall())
            return cur.fetchall()
    

    def change_email(cur, email, client_id):
        with conn.cursor() as cur:          
            cur.execute("""
                UPDATE Client
                SET email=%s 
                WHERE client_id=%s
                RETURNING client_id, first_name, last_name, email;
                """, (email, client_id, ))           
            print("Записи обновлены!")
            print(cur.fetchall())
            return cur.fetchall()
       
    
    def change_phone(cur, client_id, phone):
        with conn.cursor() as cur:          
            cur.execute("""
                UPDATE Phones
                SET phone=%s
                WHERE client_id=%s
                RETURNING client_id, phone;
                """, (client_id, phone, ))            
            print("Записи обновлены!")
            print(cur.fetchall())
            return cur.fetchall()
        
    
    def find_client(cur, first_name, last_name, email, phone):
        with conn.cursor() as cur:           
            cur.execute("""
                SELECT c.first_name, c.last_name, c.email, p.phone FROM Client c
                LEFT JOIN Phones p ON c.client_id = p.client_id
                WHERE c.first_name=%s AND c.last_name=%s AND c.email=%s AND p.phone=%s;
                """, (first_name, last_name, email, phone, ))
            print(cur.fetchall())
            return cur.fetchall()


    def delete_phone(cur, client_id, phone):
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM Phones
                WHERE client_id=%s and phone=%s 
                RETURNING client_id, phone;
                """, (client_id, phone, ))
            print("Записи удалены!")
            print(cur.fetchall())
            return cur.fetchall()

  
    def delete_client(cur, client_id):
        with conn.cursor() as cur:            
            cur.execute("""
                DELETE FROM Client
                WHERE client_id=%s;
                """, client_id, )
            print("Записи удалены!")


    def select(cur):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM Client;
                """)
            print(cur.fetchall())
            cur.execute("""
                SELECT * FROM Phones;
                """)
            print(cur.fetchall())


    print()
    print('Здравствуйте! Какую функцию надо выполнить?')
    print()
    print('"1" Создать таблицы') 
    print('"2" Добавить клиента') 
    print('"3" Добавить номер телефона клиента') 
    print('"4" Обновить данные клиента')  
    print('"5" Найти клиента по его данным')
    print('"6" Удалить номер телефона клиета') 
    print('"7" Удалить клиента') 
    print('"8" Вывести данные таблиц')
    print('"9" Выйти из программы') 
    print()
    
    while True:
        function = input('Введите нужную команду: ')
        if function == '1':
            create_db(cur)
        elif function == '2':
            first_name = input('Введите имя клиента: ')
            last_name = input('Введите фамилию клиента: ')
            email = input('Введите Email клиента: ')
            add_client(cur, first_name, last_name, email)
        elif function == '3':
            client_id = input('Введите id клиента: ')
            phone = input('Введите телефон клиента: ')   
            add_phone(cur, client_id, phone)               
        elif function == '4':
            print()
            print('Какие данные надо изменить?')
            print('"1" Имя и фамилию клиента')
            print('"2" Email клиента')
            print('"3" Телефон клиента')
            task = input('Введите нужную команду: ')
            if task == "1":
                client_id = input('Введите id клиента: ')
                first_name = input('Введите новое имя клиента: ')
                last_name = input('Введите новую фамилию клиента: ')
                change_client(cur, first_name, last_name, client_id)
            elif task == "2":
                client_id = input('Введите id клиента: ')
                email = input('Введите новый Email клиента: ')
                change_email(cur, email, client_id)
            elif task == "3":
                client_id = input('Введите id клиента: ')
                phone = input('Введите новый телефон клиента: ')
                change_phone(cur, phone, client_id)
            else:
                print('Введена неверная команда!')                
        elif function == '5':
            first_name = input('Введите имя клиента: ')
            last_name = input('Введите фамилию клиента: ')
            email = input('Введите Email клиента: ')
            phone = input('Введите телефон клиента: ')
            find_client(cur, first_name, last_name, email, phone)
        elif function == '6':
            client_id = input('Введите id клиента: ')
            phone = input('Введите телефон клиента, который надо удалить: ')
            delete_phone(cur, client_id, phone)
        elif function == '7':
            client_id = input('Введите id клиента: ')
            delete_client(cur, client_id)
        elif function == '8':
            select(cur)   
        elif function == '9':
            if conn:
                cur.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто!")
                break                               
        else:
            print('Введена неверная команда!')
