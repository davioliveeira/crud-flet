import sqlite3
conect = sqlite3.connect("src/db/produtos.db", check_same_thread=False)
cursor = conect.cursor()


def base_product():
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)
        '''
    )


base_product()
