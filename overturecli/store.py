"""
Implementation of the client's state store
"""

import sqlite3
import os

def get_store_connection():
    """
    Get a connection to the sqlite store file.

    If it doesn't already exist, it is created.
    """
    store_path = os.path.join(os.getcwd(), 'store.db')
    if not os.path.exists(store_path):
        conn = sqlite3.connect(store_path)
        conn.execute('''CREATE TABLE auth_token
                    (id INTEGER PRIMARY KEY, token TEXT)''')
        conn.execute('''CREATE TABLE analysis (
                        metadata_list_index INTEGER,
                        upload_dir TEXT,
                        id INTEGER,
                        created INTEGER,
                        files_uploaded INTEGER,
                        published INTEGER,
                        PRIMARY KEY (metadata_list_index, upload_dir)
                    )''')
        conn.commit()
        return conn
    return sqlite3.connect(store_path)

def close_store_connection(conn):
    """
    Commit and close the connection to the sqlite store file.
    """
    conn.commit()
    conn.close()

def find_or_insert_analysis(index, upload_dir):
    """
    Find the given analysis (identified by its index position in the metadata file submitted by the
    user) in the store file and return it.

    If not found, the analysis entry is created with all the upload tasks related to it set to
    "not done".
    """
    conn = get_store_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT * FROM analysis
           WHERE metadata_list_index = ? AND upload_dir = ?''',
        (index, upload_dir)
    )
    result = cursor.fetchone()
    if result is None:
        result = {
            'index': index,
            'upload_dir': upload_dir,
            'id': None,
            'created': False,
            'files_uploaded': False,
            'published': False
        }
        cursor.execute(
            '''INSERT INTO analysis (
                   metadata_list_index,
                   upload_dir,
                   id,
                   created,
                   files_uploaded,
                   published
                )
                VALUES (?,?,?,?,?,?);''',
            (index, upload_dir, None, 0, 0, 0)
        )
    else:
        result = {
            'index': result[0],
            'upload_dir': result[1],
            'id': result[2],
            'created': result[3] == 1,
            'files_uploaded': result[4] == 1,
            'published': result[5] == 1
        }
    close_store_connection(conn)
    return result

def save_analysis_creation(index, upload_dir, analysis_id):
    """
    Mark the analysis as created. Its ID is also added to the store at this point.
    """
    conn = get_store_connection()
    conn.execute(
        '''UPDATE analysis
           SET created = 1, id = ?
           WHERE metadata_list_index = ? AND upload_dir = ?;''',
        (analysis_id, index, upload_dir)
    )
    close_store_connection(conn)

def save_analysis_files_upload(index, upload_dir):
    """
    Mark that the files for the given analysis have been uploaded.
    """
    conn = get_store_connection()
    conn.execute(
        "UPDATE analysis SET files_uploaded = 1 WHERE metadata_list_index = ? AND upload_dir = ?;",
        (index, upload_dir)
    )
    close_store_connection(conn)

def save_analysis_publication(index, upload_dir):
    """
    Mark that the analysis has been published.
    """
    conn = get_store_connection()
    conn.execute(
        "UPDATE analysis SET published = 1 WHERE metadata_list_index = ? AND upload_dir = ?;",
        (index, upload_dir)
    )
    close_store_connection(conn)

def store_auth_token(token):
    """
    Store the Overture auth token after a successful login in the store.

    Note that any previous token is deleted.
    """
    conn = get_store_connection()
    conn.execute('''DELETE FROM auth_token WHERE id >= 0''')
    conn.execute('''INSERT INTO auth_token (token) VALUES(?);''', (token, ))
    close_store_connection(conn)

def get_auth_token():
    """
    Get the Overture auth token from the store.

    If no token is found, None is returned instead.
    """
    conn = get_store_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM auth_token')
    result = cursor.fetchone()
    close_store_connection(conn)
    return result[1] if result is not None else result
