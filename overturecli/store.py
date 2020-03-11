import sqlite3
import os

def get_store_connection():
    store_path = os.path.join(os.getcwd(), 'store.db')
    if not os.path.exists(store_path):
        conn = sqlite3.connect(store_path)
        conn.execute('''CREATE TABLE auth_token
                    (id INTEGER PRIMARY KEY, token TEXT)''')
        conn.execute('''CREATE TABLE analysis_status
                    (id INTEGER, upload_dir TEXT, analysis_created INTEGER, files_uploaded INTEGER, analysis_published INTEGER, PRIMARY KEY (id, upload_dir))''')
        conn.commit()
        return conn
    else:
        return sqlite3.connect(store_path)

def close_store_connection(conn):
    conn.commit()
    conn.close()

def store_auth_token(token):
    conn = get_store_connection()
    conn.execute('''DELETE FROM auth_token WHERE id >= 0''')
    conn.execute('''INSERT INTO auth_token (token) VALUES(?);''', (token, ))
    close_store_connection(conn)

def get_auth_token():
    conn = get_store_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM auth_token')
    result = cursor.fetchone()
    close_store_connection(conn)
    return result[1] if result is not None else result
