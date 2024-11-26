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

    conn.commit()
    conn.close()

def CreateCursor(database):
    """creates and returns a connection and cursor for the database supplied"""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    return conn,cursor

def isUsernameInAccounts(username,databasename):
    """return true or false based on if the username is in the accounts table or not"""
    conn,cursor = CreateCursor(databasename)

    cursor.execute("SELECT * FROM accounts WHERE username == (?)",(username,))

    matchingUsername = cursor.fetchall()
    conn.close()

    if matchingUsername != []:
        return True
    else:
        return False
    
def checkPassword(username,password, databasename):
    """check if the password for a supplied user name is correct. Returns the id if successful else Nonetype"""

    conn, cursor = CreateCursor(databasename)
    cursor.execute("SELECT * FROM accounts WHERE username == (?)", (username,))
    accounts = cursor.fetchall()
    conn.close()
    
    if password == accounts[0][2]:
        return accounts[0][0]
    else:
        return None
    
def addAccount(username,password,databasename):
    """add the supplied username and password to the accounts databse and create a foldername and add to the folder database"""

    conn, cursor = CreateCursor(databasename)

    cursor.execute("INSERT INTO accounts (username, password) VALUES (?,?)",(username,password))
    conn.commit()

    cursor.execute("SELECT account_id FROM accounts WHERE username == (?)",(username,))
    id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO folders (account_id,folderpath) VALUES (?,?)",(id,f"Memes/{id}"))
    conn.commit()
    conn.close()

def getFolderPath(id,databasename)->str:
    """returns the FolderPath of the users folder"""

    conn,cursor = CreateCursor(databasename)

    cursor.execute("SELECT folderpath FROM folders WHERE account_id == (?)",(id,))
    folderPath = cursor.fetchone()

    if folderPath != None:
        folderPath = folderPath[0]

    conn.close()

    return folderPath