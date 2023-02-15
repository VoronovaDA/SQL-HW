import psycopg2
from psycopg2 import Error


try:
    conn = psycopg2.connect(user="postgres", 
                            password="7404",
                            database="homework_db")
    cur = conn.cursor()

    cur.execute("""
                DROP TABLE Phones;
                DROP TABLE Client;
                """)

    def create_db(cur):
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
            cur.execute("""
                INSERT INTO Client(first_name, last_name, email)
                VALUES(%s, %s, %s)
                RETURNING client_id, first_name, last_name, email;
                """, (first_name, last_name, email, ))            
            print("Запись успешно добавлена ​​в таблицу!")
            print(cur.fetchone())
            return cur.fetchone()
            
        
    def add_phone(cur, client_id, phone):           
            cur.execute("""
                INSERT INTO Phones(client_id, phone)
                VALUES(%s, %s)
                RETURNING client_id, phone;
                """, (client_id, phone, ))         
            print( "Запись успешно добавлена ​​в таблицу!")
            print(cur.fetchone())
            return cur.fetchone()

        
    def change_client(cur, first_name, last_name, email, client_id):          
            cur.execute("""
                UPDATE Client
                SET first_name=%s, last_name=%s, email=%s 
                WHERE client_id=%s
                RETURNING client_id, first_name, last_name, email;
                """, (first_name, last_name, email, client_id, ))           
            print("Записи обновлены!")
            print(cur.fetchall())
            return cur.fetchall()
       
    
    def change_phone(cur, client_id, phone):          
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
            cur.execute("""
                SELECT c.first_name, c.last_name, c.email, p.phone FROM Client c
                LEFT JOIN Phones p ON c.client_id = p.client_id
                WHERE c.first_name=%s OR c.last_name=%s OR c.email=%s OR p.phone=%s;
                """, (first_name, last_name, email, phone, ))
            print(cur.fetchall())
            return cur.fetchall()


    def delete_phone(cur, client_id, phone):
            cur.execute("""
                DELETE FROM Phones
                WHERE client_id=%s and phone=%s 
                RETURNING client_id, phone;
                """, (client_id, phone, ))
            print("Записи удалены!")
            print(cur.fetchall())
            return cur.fetchall()

  
    def delete_client(cur, client_id):            
            cur.execute("""
                DELETE FROM Client
                WHERE client_id=%s;
                """, client_id, )
            print("Записи удалены!")


    def select(cur):
            cur.execute("""
                SELECT * FROM Client;
                """)
            print(cur.fetchall())
            cur.execute("""
                SELECT * FROM Phones;
                """)
            print(cur.fetchall())


    print('Создать таблицы "1" ') 
    print('Добавить клиента "2"') 
    print('Добавить номер телефона клиента "3" ') 
    print('Обновить данные клиента "4" ') 
    print('Обновить номер телефона клиента "5" ') 
    print('Найти клиента по его данным и номеру телефона "6" ')
    print('Удалить номер телефона клиета "7" ') 
    print('Удалить клиента "8" ') 
    print('Вывести данные таблиц "9"')
    print('Выйти из программы "10"') 
    
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
            client_id = input('Введите id клиента: ')
            first_name = input('Введите новое имя клиента: ')
            last_name = input('Введите новую фамилию клиента: ')
            email = input('Введите новый Email клиента: ')
            change_client(cur, first_name, last_name, email, client_id)
        elif function == '5':
            client_id = input('Введите id клиента: ')  
            phone = input('Введите новый телефон клиента: ')
            change_phone(cur, phone, client_id)
        elif function == '6':
            first_name = input('Введите имя клиента: ')
            last_name = input('Введите фамилию клиента: ')
            email = input('Введите Email клиента: ')
            phone = input('Введите телефон клиента: ')
            find_client(cur, first_name, last_name, email, phone)
        elif function == '7':
            client_id = input('Введите id клиента: ')
            phone = input('Введите телефон клиента, который надо удалить: ')
            delete_phone(cur, client_id, phone)
        elif function == '8':
            client_id = input('Введите id клиента: ')
            delete_client(cur, client_id)
        elif function == '9':
            select(cur)   
        elif function == '10':
            if conn:
                cur.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто!")     
                break          
        else:
            print('Введена неверная команда!')
            break
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
