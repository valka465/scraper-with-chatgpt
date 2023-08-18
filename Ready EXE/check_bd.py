import sqlite3

DATABASE_NAME = 'user_data'

DATABASE_URI = f'{DATABASE_NAME}.db'

connection = sqlite3.connect(DATABASE_URI)

cursor = connection.cursor()

try:
    cursor.execute('SELECT name FROM sqlite_master;')
    print(f"Database '{DATABASE_NAME}' is already exists.")

    cursor.execute("SELECT scrapeitapi FROM user;")
    result = cursor.fetchone()

    if result:
        print(f"Table 'user' is already exists in '{DATABASE_NAME}'.")
    else:
        cursor.execute("""CREATE TABLE user
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                scrapeitapi TEXT, 
                gptapi TEXT)
            """)
        
        print(f"Table 'user' doesn't exist in '{DATABASE_NAME}'")
except sqlite3.OperationalError:
    cursor.execute("""CREATE TABLE user
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                scrapeitapi TEXT, 
                gptapi TEXT)
            """)
    print(f"DB '{DATABASE_NAME}' is created.")

cursor.close()
connection.commit()

connection.close()
