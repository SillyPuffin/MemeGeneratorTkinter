import sqlite3
import shutil
from os import walk
from os import path

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

def GenDatabase(databasename):
    """if the database given does not exist create it"""
    conn = sqlite3.connect(databasename)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    conn.close()

    if not tables:
        ResetDatabases(databasename)

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

def deleteAccount(id, databasename):
    """delete the account corresponding to the id"""
    conn, cursor = CreateCursor(databasename)

    cursor.execute("SELECT folderpath FROM folders WHERE account_id == (?)",(id,))
    foldername = cursor.fetchone()
    foldername = foldername[0]

    try:
        shutil.rmtree(foldername)
    except FileNotFoundError:
        print(f"file not found {foldername}")
    except Exception as e:
        print(f"error deleteing account {id}")

    cursor.execute("DELETE FROM accounts WHERE account_id == (?)",(id,))
    
    conn.commit()
    conn.close()

def getAccountId(username,password, databasename)->int:
    """returns the account id of a given username and password"""
    conn,cursor = CreateCursor(databasename)

    cursor.execute("SELECT account_id FROM accounts WHERE username == (?) and password== (?)",(username,password))
    id = cursor.fetchone()

    conn.close()

    if id != None:
        id = id[0]

    return id

def getFolderPath(id,databasename)->str:
    """returns the FolderPath of the users folder"""

    conn,cursor = CreateCursor(databasename)

    cursor.execute("SELECT folderpath FROM folders WHERE account_id == (?)",(id,))
    folderPath = cursor.fetchone()
    if folderPath != None:
        folderPath = folderPath[0]

    conn.close()

    return folderPath

def moveFile(filename, src_path, dst_path):
    """move a given filename from a source to a destination, renaming if one already exists"""
    suffix = filename[-4:]
    cutname = filename[0:-4]
    finalname = filename

    count = 1
    while path.exists(dst_path +'/' + finalname):
        finalname = f"{cutname} ({count}){suffix}"
        count+=1

    dest_path = dst_path +"/"+ finalname

    shutil.move(src_path, dest_path)

def copyFile(filename, src_path, dst_path):
    """copy the file from the source path to the destination path"""
    suffix = filename[-4:]
    cutname = filename[0:-4]
    finalname = filename
    count = 1

    while path.exists(dst_path +'/' + finalname):
        finalname = f"{cutname} ({count}){suffix}"
        count+=1

    dest_path = dst_path +"/" + finalname

    shutil.copy(src_path, dest_path)

def saveImage(image, filename , dst_path):
    """save the file into the dst path"""

    suffix = filename[-4:]
    cutname = filename[0:-4]
    finalname = filename
    count = 1

    while path.exists(dst_path + '/' + finalname):
        finalname = f"{cutname} ({count}){suffix}"
        count+=1

    dest_path = dst_path +"/" + finalname

    image.save(dest_path)

    print(f"saving {filename} to {dest_path}")

def deleteImage(image_path, id, databasename):
    """remove the selected image and place it in the bin folder"""

    prefix = getFolderPath(id,databasename)

    src_path = prefix + "/" + image_path
    dst_path = "recyclebin"

    moveFile(image_path, src_path, dst_path)

def deleteAllImages(image_dir):
    """move all the images in a directory to the bin"""
    files = list(walk(image_dir))
    if files:
        filenames = files[0][2]
        for name in filenames:
            fullpath = image_dir +"/" +  name
            dst_path = "recyclebin"

            moveFile(name, fullpath, dst_path)

def getAllAccounts(id, databasename):
    """return a list of all accounts as the username and id in a tuple except the id passed in"""
    conn, cursor = CreateCursor(databasename)

    cursor.execute("SELECT account_id, username FROM accounts WHERE account_id != (?)",(id,))
    accounts = cursor.fetchall()
    conn.close()

    return accounts