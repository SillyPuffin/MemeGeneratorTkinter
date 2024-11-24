import sqlite3

def ResetDatabases(databasename):
    #delete all tables
    conn = sqlite3.connect(databasename)
    conn.execute("DROP TABLE IF EXISTS accounts")
    conn.execute("DROP TABLE IF EXISTS folders")
    conn.commit()
    conn.close()

    #recreate the tables
    conn,cursor = CreateCursor(databasename)
    
    cursor.execute("""
    CREATE TABLE accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,    
        username TEXT NOT NULL,
        password TEXT NOT NULL
                   );
    """)

    cursor.execute("""
    CREATE TABLE folders (
        account_id INTEGER NOT NULL,    
        folderpath TEXT NOT NULL
                   );
    """)


def CreateCursor(tablename):
    """creates and returns a connection and cursor for the table name supplied"""
    conn = sqlite3.connect(tablename)
    cursor = conn.cursor()
    return conn,cursor